/*!
 * JavaScript for FeTSy
 * Copyright (c) 2015 Norman Jäckel
 * Licensed under the MIT License
 */

(function () {

'use strict';

var baseRestUrl = 'rest';

var app = angular.module( 'FeTSy', [ 'ngCookies', 'ui.bootstrap' ] );


app.run([ '$http', '$cookies', function ( $http, $cookies ) {
    // Add CSRF token from csrftoken cookie to relevant HTTP headers as X-CSRFToken.
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


app.controller( 'TicketListCtrl', function ( $http, $modal ) {
    var ticketCtrl = this;

    // Service that fetches all status data from the REST API.
    $http.get([ baseRestUrl, 'status', '' ].join('/'))
        .success(function ( data, status, headers, config ) {
            // Add data to the scope.
            ticketCtrl.allStatus = data;
        })

        .error(function ( data, status, headers, config ) {
            alert('There was an error. Please reload the page.');
        });

    // Service that fetches all users data from the REST API.
    $http.get([ baseRestUrl, 'users', '' ].join('/'))
        .success(function ( data, status, headers, config ) {
            // Add data to the scope.
            ticketCtrl.allUsers = data;
        })

        .error(function ( data, status, headers, config ) {
            alert('There was an error. Please reload the page.');
        });

    // Setup Ticket constructor.
    var Ticket = function ( data ) {
        var ticket = this;

        // Add REST API data to ticket.
        for ( var key in data ) {
            ticket[key] = data[key];
        }

        // Add tmpContent property. This is only used for the change form and
        // updated via AngularJS's magic.
        ticket.tmpContent = ticket.content;
    };

    // Limit of length of content in the table. If the content is longer, some
    // dots are added.
    ticketCtrl.limit = 50;

    // Add isLong function to deterine whether to print dots in content cell.
    Ticket.prototype.isLong = function () {
        var ticket = this;
        return ticket.content.length > ticketCtrl.limit;
    };

    // Add change function. The argument newData is required. These data are
    // sent to the REST API. If you supply the toScope argument, these data are
    // used to fill the scope instead of the given data. The response from the
    // REST API is not used.
    Ticket.prototype.change = function ( newData, toScope ) {
        var ticket = this;
        $http.patch( [ baseRestUrl, 'tickets', ticket.id, '' ].join('/'), newData )
            .success(function ( data, status, headers, config ) {
                if ( toScope !== undefined ) {
                    newData = toScope;
                }
                for ( var field in newData ) {
                    ticket[field] = newData[field];
                }
            })

            .error(function ( data, status, headers, config ) {
                alert('There was an error. Please reload the page.');
            });
    };

    // Add destroy function.
    Ticket.prototype.destroy = function () {
        var ticket = this;
        $http.delete([ baseRestUrl, 'tickets', ticket.id, '' ].join('/'))
            .success(function ( data, status, headers, config ) {
                var index = ticketCtrl.tickets.indexOf( ticket );
                ticketCtrl.tickets.splice( index, 1 );
            })

            .error(function ( data, status, headers, config ) {
                alert('There was an error. Please reload the page.');
            });
    };

    // Add popover button function for info on tickets.
    Ticket.prototype.popOver = function ( $event ) {
        var ticket = this;
        var button = $($event.target);
        button.popover('destroy');
        button.popover({
            'title': 'Ticket #' + ticket.id,
            'placement': 'left'
        }).popover('show');
        button.next().click(function ( event ) {
            button.popover('destroy');
            event.preventDefault();
        });
    };

    // Service that fetches all ticket data from the REST API.
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

    // Setup table headers.
    ticketCtrl.headers = [
        { 'key': 'id', 'verboseName': '#' },
        { 'key': 'content', 'verboseName': 'Content' },
        { 'key': 'status', 'verboseName': 'Status' },
        { 'key': 'assignee', 'verboseName': 'Assignee' }
    ];

    // Table filtering
    ticketCtrl.filter = undefined;

    // Table sorting
    ticketCtrl.sortColumn = 'id';
    ticketCtrl.reverse = true;
    ticketCtrl.toggleSort = function ( index ) {
        if ( ticketCtrl.sortColumn === ticketCtrl.headers[index].key ) {
            ticketCtrl.reverse = !ticketCtrl.reverse;
        }
        ticketCtrl.sortColumn = ticketCtrl.headers[index].key;
    };

    // Form for a new ticket via angular ui bootstrap modal.
    ticketCtrl.newTicketForm = function () {
        var modalInstance = $modal.open({
            templateUrl: 'newTicketForm.html',
            controller: 'NewTicketFormModalCtrl as newTicketFormModalCtrl'
        });
        modalInstance.result.then(function ( content ) {
            $http.post( [ baseRestUrl, 'tickets', '' ].join('/'), { 'content': content, 'status': ticketCtrl.allStatus[0].name } )
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
