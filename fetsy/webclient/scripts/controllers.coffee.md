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
                    (@paginationPage - 1) * @itemsPerPage
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

Append a controller for the row with the 'New Ticket' button, the
checkboxes and the search bar.

    .controller 'TopRowCtrl', [
        '$uibModal'
        '$wamp'
        'userHasPermissionFactory'
        'ticketFilterValues'
        ($uibModal, $wamp, userHasPermissionFactory, ticketFilterValues) ->

Hook for the button to create a new ticket. The uib-modal directive from
Angular UI Bootstrap is used.

            @newTicketForm =
                if userHasPermissionFactory.canAddTicket
                    ->
                        modalInstance = $uibModal.open
                            templateUrl: 'newTicketForm.html'
                            controller: 'NewTicketFormCtrl as newTicketForm'

                        modalInstance.result.then (result) ->
                                $wamp.call 'org.fetsy.createTicket', [],
                                    object:
                                        content: result.content
                                        period: result.period
                                .then (result) ->
                                    if result.type == 'success'
                                        console.log(
                                            'WAMP message: ' + result.details
                                        )
                                    else
                                        console.error(
                                            'WAMP error: ' + result.details
                                        )
                                    return
                                return
                        return
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

            @headers = [
                new ticketListHeaderFactory.Header
                    sortKey: 'id'
                    col: '1'
                    displayName: 'Number'

                new ticketListHeaderFactory.Header
                    sortKey: 'content'
                    col: '4'
                    displayName: 'Content'
                    icon: 'cog'

                new ticketListHeaderFactory.Header
                    sortKey: 'status'
                    col: '1'
                    displayName: 'Status'
                    icon: 'star'

                new ticketListHeaderFactory.Header
                    sortKey: 'priority'
                    col: '1'
                    displayName: 'Priority'
                    icon: 'fire'

                new ticketListHeaderFactory.Header
                    sortKey: 'assignee'
                    col: '2'
                    displayName: 'Assignee'
                    icon: 'user'

                new ticketListHeaderFactory.Header
                    sortKey: 'period'
                    col: '2'
                    displayName: ->
                        if ticketFilterValues.remainingTime
                            'Period (in minutes)'
                        else
                            'Deadline'
                    icon: ->
                        if ticketFilterValues.remainingTime
                            'hourglass'
                        else
                            'time'
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


## Controller for the modal for new tickets

Append a controller for the modal for new tickets.

    .controller 'NewTicketFormCtrl', [
        '$uibModalInstance'
        'ticketFilterValues'
        'defaultPeriod'
        ($uibModalInstance, ticketFilterValues, defaultPeriod) ->

            @remainingTimeValue = ticketFilterValues.remainingTime

Default value for the periodOrDeadlineField.

            @periodOrDeadlineField =
                if @remainingTimeValue
                    String(defaultPeriod)
                else
                    moment()
                    .add defaultPeriod, 'minutes'
                    .format 'YYYY-MM-DD HH:mm'


Hook for the save button. This validates the input and closes the modal.
The validated data are handled back to the TopRowCtrl.

            @save = ->

Validate period or deadline input field depending on remainingTimeValue flag.

                if @remainingTimeValue
                    period = parseInt @periodOrDeadlineField
                else
                    parsedDate = moment @periodOrDeadlineField
                    if parsedDate.isValid()
                        period = parsedDate.diff moment(), 'minutes'

Hint: We add one minute here to get correct time because the seconds are stripped off above.

                        period++

Save ticket if the period or deadline field is valid and there is some
content.

                if @contentField and period or period is 0
                    $uibModalInstance.close
                        'content': @contentField
                        'period': period
                else
                    $uibModalInstance.dismiss 'cancel'
                return

Hook for the cancel button. This does only close the modal.

            @cancel = ->
                $uibModalInstance.dismiss 'cancel'
                return

            return
    ]


## Controller for the modal for the ticket info

Append a controller for the modal for the ticket info.

    .controller 'TicketInfoCtrl', [
        '$uibModalInstance'
        '$wamp'
        'ticket'
        ($uibModalInstance, $wamp, ticket) ->
            @ticket = ticket

Hook for the delete button. This closes the modal.

            @delete = ->
                $wamp.call 'org.fetsy.deleteTicket', [],
                    id: ticket.id
                .then (result) ->
                    if result.type == 'success'
                        console.log(
                            'WAMP message: ' + result.details
                        )
                    else
                        console.error(
                            'WAMP error: ' + result.details
                        )
                    return
                $uibModalInstance.close()
                return

Hook for the cancel button. This does only close the modal.

            @cancel = ->
                $uibModalInstance.dismiss 'cancel'
                return

            return
    ]


## Controller for the tag administration top row.

Append a controller for the row with the 'New Tag' button.

    .controller 'TagAdministrationTopRowCtrl', [
        '$uibModal'
        '$wamp'
        'userHasPermissionFactory'
        ($uibModal, $wamp, userHasPermissionFactory) ->

Hook for the button to create a new tag. The uib-modal directive from
Angular UI Bootstrap is used.

            @newTagForm =
                if userHasPermissionFactory.isStaff
                    ->
                        modalInstance = $uibModal.open
                            templateUrl: 'newTagForm.html'
                            controller: 'NewTagFormCtrl as newTagForm'

                        modalInstance.result.then (result) ->
                                $wamp.call 'org.fetsy.createTag', [],
                                    object:
                                        name: result.name
                                        color: result.color
                                        weight: result.weight
                                .then (result) ->
                                    if result.type == 'success'
                                        console.log(
                                            'WAMP message: ' + result.details
                                        )
                                    else
                                        console.error(
                                            'WAMP error: ' + result.details
                                        )
                                    return
                                return
                        return
                else
                    null
            return
    ]


## Controller for the tag administration.

Append a controller for the administration of ticket tags.

    .controller 'TagAdministrationCtrl', [
        '$scope'
        'DS'
        ($scope, DS) ->

Append all tags to the body.

            watchExpression = -> DS.lastModified('Tag')
            listener = =>
                @tags = DS.getAll 'Tag'
                return
            $scope.$watch watchExpression, listener

            return
    ]


## Controller for the modal for new tags

Append a controller for the modal for new tags.

    .controller 'NewTagFormCtrl', [
        '$uibModalInstance'
        ($uibModalInstance) ->

Default value for the colorField.

            @colorField = 'default'

Hook for the save button. This validates the input and closes the modal.
The validated data are handled back to the TagAdministrationTopRowCtrl.

            @save = ->
                if @nameField
                    $uibModalInstance.close
                        'name': @nameField
                        'color': @colorField
                        'weight': 0
                else
                    $uibModalInstance.dismiss 'cancel'
                return

Hook for the cancel button. This does only close the modal.

            @cancel = ->
                $uibModalInstance.dismiss 'cancel'
                return

            return
    ]
