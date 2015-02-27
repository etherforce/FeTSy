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
    // Add CSRF token from cookie to relevant HTTP headers.
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

    // Limit of length of content in the table. If the content is longer, a
    // popover button is added.
    ticketCtrl.limit = 50;

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


    // Service that fetches all ticket data from the REST API.
    $http.get([ baseRestUrl, 'tickets', '' ].join('/'))
        .success(function ( data, status, headers, config ) {
            // Setup table headers.
            ticketCtrl.headers = [
                { 'key': 'id', 'verboseName': '#' },
                { 'key': 'content', 'verboseName': 'Content' },
                { 'key': 'status', 'verboseName': 'Status' },
                { 'key': 'assignee', 'verboseName': 'Assignee' }
            ];

            // Add several ticket properties.
            angular.forEach( data, function ( ticket ) {
                // Add change property.
                ticket.change = function ( newData, toScope ) {
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

                // Add delete property.
                ticket.destroy = function () {
                    $http.delete([ baseRestUrl, 'tickets', ticket.id, '' ].join('/'))
                        .success(function ( data, status, headers, config ) {
                            var index = ticketCtrl.tickets.indexOf( ticket );
                            ticketCtrl.tickets.splice( index, 1 );
                        })

                        .error(function ( data, status, headers, config ) {
                            alert('There was an error. Please reload the page.');
                        });
                };

                // Add tmpContent property.
                ticket.tmpContent = ticket.content;

                // Add popover button to long tickets.
                ticket.isLong = function () {
                    return ticket.content.length > ticketCtrl.limit;
                };
                ticket.popOver = function ( $event ) {
                    var button = $($event.target);
                    button.popover('destroy');
                    button.popover({ 'title': 'Ticket #' + ticket.id }).popover('show');
                    button.next().click(function ( event ) {
                        button.popover('destroy');
                        event.preventDefault();
                    });
                };
            });

            // Finally add modified data to the scope.
            ticketCtrl.tickets = data;
        })

        .error(function ( data, status, headers, config ) {
            alert('There was an error. Please reload the page.');
        });

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
                    ticketCtrl.tickets.push( data );
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
