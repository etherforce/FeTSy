/*!
 * JavaScript for FeTSy
 * Copyright (c) 2015 Norman Jäckel
 * Licensed under the MIT License
 */

(function () {

'use strict';

var app = angular.module( 'FeTSy', [ 'ngCookies', 'ui.bootstrap', 'btorfs.multiselect' ] );


// Add CSRF token from csrftoken cookie to relevant HTTP headers as X-CSRFToken.
app.run([ '$http', '$cookies', function ( $http, $cookies ) {
    var methods = [ 'post', 'put', 'patch', 'delete' ];
    for ( var i = 0; i < methods.length; ++i ) {
        var headers = $http.defaults.headers[methods[i]];
        if ( headers === undefined ) {
            $http.defaults.headers[methods[i]] = { 'X-CSRFToken': $cookies.csrftoken };
        } else {
            headers['X-CSRFToken'] = $cookies.csrftoken;
        }
    }
} ]);


// Setup TicketListCtrl, the main controller for this project.
app.controller( 'TicketListCtrl', function ( $http, $modal ) {
    var ticketCtrl = this;

    // Service that fetches all users data from the REST API.
    $http.get([ baseRestUrl, 'users', '' ].join('/'))
        .success(function ( data, status, headers, config ) {
            ticketCtrl.allUsers = data;
        })

        .error(function ( data, status, headers, config ) {
            alert('There was an error. Please reload the page.');
        });

    // Setup Ticket constructor.
    // Add REST API data to ticket and update properties.
    var Ticket = function ( data ) {
        var ticket = this;
        angular.extend(ticket, data);
        ticket.updateProperties();
    };

    // Helper function to update some calculated properties.
    Ticket.prototype.updateProperties = function () {
        var ticket = this;

        // Caluclate deadline time delta.
        var created = new Date(ticket.created);
        var timeToEnd = (created.getTime() + ticket.deadline * 60 * 1000 - Date.now()) / 1000 / 60;
        ticket.timeToEnd = Math.trunc(timeToEnd);

        // Add tmpContent, tmpTags and tmpDeadline properties. These are only
        // used for the change form and updated via AngularJS's magic.
        ticket.tmpContent = ticket.content;
        ticket.tmpTags = ticket.tags;
        ticket.tmpDeadline = ticket.deadline;
    };

    // Limit of length of content in the table. If the content is longer, some
    // dots are added.
    ticketCtrl.limit = 30;

    // Add isLong function to determine whether to print dots in content cell.
    Ticket.prototype.isLong = function () {
        var ticket = this;
        return ticket.content.length > ticketCtrl.limit;
    };

    // Add change function. The argument changedData is required. These data are
    // sent to the REST API.
    Ticket.prototype.change = function ( changedData ) {
        var ticket = this;
        $http.patch( [ baseRestUrl, 'tickets', ticket.id, '' ].join('/'), changedData )
            .success(function ( data, status, headers, config ) {
                angular.extend(ticket, data);
                ticket.updateProperties()
            })
            .error(function ( data, status, headers, config ) {
                alert('There was an error. Please reload the page.');
            });
    };

    // Add popover button function for info on tickets.
    //
    // TODO use angular ui bootstrap.
    //
    Ticket.prototype.popOver = function ( $event ) {
        var ticket = this;
        var button = $($event.target);
        var created = new Date(ticket.created);
        button.popover('destroy');
        button.popover({
            'title': 'Ticket #' + ticket.id + ' | ' + created.toLocaleString(),
            'content': ticket.content,
            'placement': 'left'
        }).popover('show');
        button.next().click(function ( event ) {
            button.popover('destroy');
            event.preventDefault();
        });
    };

    // Service that fetches all ticket data from the REST API.
    // First it fetches Options from the REST API and save them into ticketCtrl.options.
    $http({ 'method': 'OPTIONS', 'url': [ baseRestUrl, 'tickets', '' ].join('/') })
        .success(function ( data, status, headers, config ) {
            // Save option data.
            ticketCtrl.options = data;
            // Save special rendered tag options to ticketCtrl.allTags.
            ticketCtrl.allTags = [];
            angular.forEach(ticketCtrl.options.actions.POST.tags.choices, function ( value ) {
                ticketCtrl.allTags.push({ 'name': value.value.match(/'name': '([\w]*)'/)[1] });
            });
            // Now fetch all other data.
            $http.get([ baseRestUrl, 'tickets', '' ].join('/'))
                .success(function ( data, status, headers, config ) {
                    // Construct tickets and push them to scope.
                    ticketCtrl.tickets = [];
                    for (var index in data) {
                        var ticket = new Ticket(data[index]);
                        ticketCtrl.tickets.push(ticket);
                    }
                })
                .error(function ( data, status, headers, config ) {
                    alert('There was an error. Please reload the page.');
                });
        })
        .error(function ( data, status, headers, config ) {
            alert('There was an error. Please reload the page.');
        });

    // Setup table headers.
    ticketCtrl.headers = [
        { 'key': 'id', 'verboseName': 'Id', 'cssIconClass': 'glyphicon-tag' },
        { 'key': 'content', 'verboseName': 'Content', 'cssIconClass': 'glyphicon-cog' },
        { 'key': 'status', 'verboseName': 'Status', 'cssIconClass': 'glyphicon-record' },
        { 'key': 'priority', 'verboseName': 'Priority', 'cssIconClass': 'glyphicon-fire' },
        { 'key': 'assignee.name', 'verboseName': 'Assignee', 'cssIconClass': 'glyphicon-user' },
        { 'key': 'timeToEnd', 'verboseName': 'Deadline', 'cssIconClass': 'glyphicon-time' }
    ];

    // Setup table filtering using the checkboxes and the search filter.
    ticketCtrl.search = undefined;
    ticketCtrl.showClosed = false;
    ticketCtrl.filtering = function ( value, index ) {
        return ticketCtrl.showClosed || value.status !== 'closed';
    };

    // Setup table sorting
    ticketCtrl.sortColumn = 'id';
    ticketCtrl.reverse = true;
    ticketCtrl.toggleSort = function ( index ) {
        if ( ticketCtrl.sortColumn === ticketCtrl.headers[index].key ) {
            ticketCtrl.reverse = !ticketCtrl.reverse;
        }
        ticketCtrl.sortColumn = ticketCtrl.headers[index].key;
    };

    // Setup form for a new ticket via angular ui bootstrap modal.
    ticketCtrl.newTicketForm = function () {
        var modalInstance = $modal.open({
            templateUrl: 'newTicketForm.html',
            controller: 'NewTicketFormModalCtrl as newTicketFormModalCtrl'
        });
        modalInstance.result.then(function ( content ) {
            var dataToSend = {
                'content': content,
                'status': ticketCtrl.options.actions.POST.status.choices[0].value,
                'tags': []
            }
            $http.post( [ baseRestUrl, 'tickets', '' ].join('/'), dataToSend )
                .success(function ( data, status, headers, config ) {
                    var ticket = new Ticket(data);
                    ticketCtrl.tickets.push(ticket);
                })
                .error(function ( data, status, headers, config ) {
                    alert('There was an error. Please reload the page.');
                });
        });
    };
});


// Setup controler for form for a new ticket (NewTicketFormModalCtrl).
app.controller( 'NewTicketFormModalCtrl', function ( $modalInstance ) {
    this.save = function () {
        if ( this.content ) {
            $modalInstance.close(this.content);
        } else {
            $modalInstance.dismiss('cancel');
        }
    };
    this.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});


}());
