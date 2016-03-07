# Base file for FeTSy controllers

Initiate new angular module with the name 'FeTSy.controllers'. Load
ui.bootstrap (Angular UI Bootstrap from the bower package
angular-bootstrap) as dependency.

    angular.module 'FeTSy.controllers', [
        'ui.bootstrap'
    ]


## Controller for navigation bar at the top of the page

Append a controller for the top navigation bar with login and logout button.

    .controller 'NavbarCtrl', [
        'userHasPermissionFactory'
        (userHasPermissionFactory) ->
            @userIsStaff = userHasPermissionFactory.isStaff
            return
    ]


## Controller for connection message

Append a controller for the message about the established connection short
after the top navigation bar.

    .controller 'ConnectionMessageCtrl', [
        '$scope'
        '$wamp'
        ($scope, $wamp) ->

Just show that the connection is open at the moment. The uib-alert directive
from Angular UI Bootstrap is used for this.

            watchExpression = -> $wamp.connection.isConnected
            listener = =>
                @connectionOpen = $wamp.connection.isConnected
                return
            $scope.$watch watchExpression, listener

            return
    ]


## Controller for pagination bar

Append a controller for the pagination bar.

    .controller 'PaginationCtrl', [
        '$scope'
        'DS'
        'ticketFilterValues'
        ($scope, DS, ticketFilterValues) ->

The uib-pagination directive from Angular UI Bootstrap is used. Here we get
the settings out of our `ticketFilterValues` store and the hook for the
change event.

            @itemsPerPage = ticketFilterValues.itemsPerPage
            @change = =>
                ticketFilterValues.paginationBegin =
                    (@.paginationPage - 1) * @.itemsPerPage
                return

Here we add a watcher to get the number of all tickets.

            watchExpression = -> DS.lastModified('Ticket')
            listener = =>
                @totalItems = DS.getAll 'Ticket'
                    .length
                return
            $scope.$watch watchExpression, listener

            return
    ]


## Controller for the top row

Append a controller for the row with the new button, the checkboxes and
the search bar.

    .controller 'TopRowCtrl', [
        '$uibModal'
        '$wamp'
        'userHasPermissionFactory'
        'ticketFilterValues'
        ($uibModal, $wamp, userHasPermissionFactory, ticketFilterValues) ->

Hook for the button to create a new ticket. Does nothing at the moment.
Should open a form later. TODO: Add form

            @newTicketForm =
                if userHasPermissionFactory.canAddTicket
                    ->
                        $wamp.call 'org.fetsy.newTicket', [],
                            ticket:
                                content: Math.random().toString()
                        .then (result) ->
                            if result.type == 'success'
                                console.log 'WAMP message: ' + result.details
                            else
                                console.error 'WAMP error: ' + result.details
                        return

                    #modalInstance = $uibModal.open
                    #    animation: true
                    #    templateUrl: 'myModalContent.html'
                    #    controller: 'NewTicketFormCtrl'

                    #modalInstance.result.then (
                    #    (result) ->
                    #        console.log foo
                    #        return
                    #    (reason) ->
                    #        console.log reason
                    #        return
                    #)
                else
                    null

Values and change event hooks for the two checkboxes: 'Show remaining time
in minutes checkbox' and 'Hide closed tickets checkbox'.

            @remainingTimeValue = ticketFilterValues.remainingTime
            @remainingTimeChange = =>
                ticketFilterValues.remainingTime = @remainingTimeValue
                return

            @closedValue = ticketFilterValues.closed
            @closedChange = =>
                ticketFilterValues.closed = @closedValue
                return

Value and change event hook for the search/filter input field/bar.

            @searchValue = ticketFilterValues.search
            @searchChange = =>
                ticketFilterValues.search = @searchValue
                return

            return
    ]


## Controller for the ticket list/ticket table

Append a controller for the ticket list/ticket table.

    .controller 'TicketListCtrl', [
        '$scope'
        'DS'
        'ticketFilterValues'
        'ticketListHeaderFactory'
        ($scope, DS, ticketFilterValues, ticketListHeaderFactory) ->

Setup values as given by the pagination bar and top functionality row to
control the filters used in the ngRepeat directive.

            @itemsPerPage = ticketFilterValues.itemsPerPage
            @getPaginationBegin = ->
                ticketFilterValues.paginationBegin
            @getSearch = ->
                ticketFilterValues.search
            @closedFilter = (value, index) ->
                not ticketFilterValues.closed or value.status isnt 'Closed'

Setup the headers of the ticket list/table. Use some fix initial values.
Setup the default sorting: first column with reversed sorting.
TODO: Change hourglass icon to time in some circumstances.

            @headers = [
                new ticketListHeaderFactory.Header
                    sortKey: 'id'
                    displayName: 'Number'
                    col: '1'

                new ticketListHeaderFactory.Header
                    sortKey: 'content'
                    displayName: 'Content'
                    col: '4'
                    icon: 'cog'

                new ticketListHeaderFactory.Header
                    sortKey: 'status'
                    displayName: 'Status'
                    col: '1'
                    icon: 'star'

                new ticketListHeaderFactory.Header
                    sortKey: 'priority'
                    displayName: 'Priority'
                    col: '1'
                    icon: 'fire'

                new ticketListHeaderFactory.Header
                    sortKey: 'assignee'
                    displayName: 'Assignee'
                    col: '2'
                    icon: 'user'

                new ticketListHeaderFactory.Header
                    sortKey: 'periodOrDeadline'
                    displayName: 'Period or deadline'
                    col: '2'
                    icon: 'hourglass'  # 'time'
            ]
            @sortColumn = 'id'
            @reverse = true

Hook for the click event on the header to change the sorting. Changes the
sorted column or the direction.

            @toggleSort = (sortKey) =>
                if @sortColumn is sortKey
                    @reverse = not @reverse
                else
                    @sortColumn = sortKey
                return

Append all tickets to the body.

            watchExpression = -> DS.lastModified('Ticket')
            listener = =>
                @all = DS.getAll 'Ticket'
                return
            $scope.$watch watchExpression, listener

            return
    ]
