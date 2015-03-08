(function () {

'use strict';

angular.module( 'FeTSyTicketControllers', [ 'ui.bootstrap', 'FeTSyTicketTableHead' ] )

// Setup TicketListCtrl, the main controller for this project.
.controller( 'TicketListCtrl', [
    '$document',
    '$http',
    '$modal',
    '$q',
    '$timeout',
    'setupTableSearchAndSort',
    function ( $document, $http, $modal, $q, $timeout, setupTableSearchAndSort ) {
        var ticketCtrl = this;

        // Setup ticket manage permission for the current user. Get the
        // permission info from the rendered template.
        ticketCtrl.userAddPerm = userPerms['fetsy.add_ticket'];
        ticketCtrl.userChangePerm = userPerms['fetsy.change_ticket'];

        // Setup empty tag array. It is filled later during an OPTIONS request.
        ticketCtrl.allTags = [];

        // Run setupTableSearchAndSort factory.
        setupTableSearchAndSort(ticketCtrl);

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

            // Add tmpContent, tmpTags and tmpDeadline properties. These are
            // only used for the change form and updated via AngularJS's magic.
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
                    ticket.updateProperties();
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

        // TODO: Move this to an extra service.
        //
        // Fetch all ticket data from the REST API.
        // First it fetches Options from the REST API and save them into
        // ticketCtrl.options. Uses a timeout to check whether the user is
        // idle and fetches data from server again.

        // Timeout and watching.
        ticketCtrl.startWatch = function () {
            var timer = $timeout(function () {}, 5000);
            timer.then(
                function () {
                    ticketCtrl.fetch();
                },
                function () {
                    ticketCtrl.startWatch();
                }
            );
            var events = 'mousemove keydown DOMMouseScroll mousewheel mousedown touchstart touchmove scroll';
            $document.find('body').on(events, function() {
                $document.find('body').off(events);
                $timeout.cancel(timer);
            });
        };

        // Fetching all ticket data.
        ticketCtrl.fetch = function () {
            $http.get([ baseRestUrl, 'tickets', '' ].join('/'))
                .success(function ( data, status, headers, config ) {
                    // Construct tickets and push them to scope.
                    ticketCtrl.tickets = [];
                    for (var index in data) {
                        var ticket = new Ticket(data[index]);
                        ticketCtrl.tickets.push(ticket);
                    }
                    ticketCtrl.startWatch();
                })
                .error(function ( data, status, headers, config ) {
                    alert('There was an error. Please reload the page.');
                });
        };

        // Fetching options for list URL.
        ticketCtrl.optionsFetch = function ( isRetrieveOptionsFetch ) {
            var methodKey = isRetrieveOptionsFetch ? 'PUT' : 'POST';
            var url = [ baseRestUrl, 'tickets', '' ].join('/');
            if ( isRetrieveOptionsFetch ) {
                url +=  '1/';
            }
            return $http({ 'method': 'OPTIONS', 'url': url })
                .success(function ( data, status, headers, config ) {
                    // Save option data. Copy data for te key POST or PUT to the key METHOD.
                    ticketCtrl.options = data;
                    ticketCtrl.options.actions.METHOD = ticketCtrl.options.actions[methodKey];
                    // Save special rendered tag options to ticketCtrl.allTags.
                    angular.forEach(ticketCtrl.options.actions.METHOD.tags.choices, function ( value ) {
                        ticketCtrl.allTags.push({ 'name': value.value.match(/'name': '([\w]*)'/)[1] });
                    });
                })
                .error(function ( data, status, headers, config ) {
                    alert('There was an error. Please reload the page.');
                });
        };

        // Now go: Make single options fetch and then ticket fetch and start timeout.
        var promisses = [];
        if ( ticketCtrl.userAddPerm ) {
            promisses.push(ticketCtrl.optionsFetch(false));
        } else if ( ticketCtrl.userChangePerm ) {
            promisses.push(ticketCtrl.optionsFetch(true));
        }
        $q.all(promisses).then(ticketCtrl.fetch);

        // Setup form for a new ticket via angular ui bootstrap modal.
        ticketCtrl.newTicketForm = function () {
            var modalInstance = $modal.open({
                templateUrl: 'newTicketForm.html',
                controller: 'NewTicketFormModalCtrl as newTicketFormModalCtrl'
            });
            modalInstance.result.then(function ( dataToSend ) {
                dataToSend.status = ticketCtrl.options.actions.METHOD.status.choices[0].value;
                dataToSend.tags = [];
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

        // Fetch all users data from the REST API.
        //
        // TODO: Remove this code and get users from options choices.
        //
        $http.get([ baseRestUrl, 'users', '' ].join('/'))
            .success(function ( data, status, headers, config ) {
                ticketCtrl.allUsers = data;
            })

            .error(function ( data, status, headers, config ) {
                alert('There was an error. Please reload the page.');
            });
    }
])

// Setup controler for form for a new ticket (NewTicketFormModalCtrl).
.controller( 'NewTicketFormModalCtrl', [
    '$modalInstance',
    function ( $modalInstance ) {
        // Default deadline is 120 minutes.
        this.deadline = 120;
        this.save = function () {
            if ( this.content ) {
                $modalInstance.close({ 'content': this.content, 'deadline': this.deadline });
            } else {
                $modalInstance.dismiss('cancel');
            }
        };
        this.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    }
]);

}());
