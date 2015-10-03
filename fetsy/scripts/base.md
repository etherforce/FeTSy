# Base file

## Angular Module

Initiate new angular module. Use ui.bootstrap as dependency.

    angular.module 'FeTSy', [
        'ui.bootstrap'
    ]


## Services

### User's Permission factory

Append a factory recipe to the app which keeps the user's permissions.

    .factory 'userHasPermissionFactory', [
        ->
            canAddTicket: true
            canChangeTicket: true
            isStaff: true
    ]


### Values for ticket list filtering

Append a value recipe to the app which stores values to controll the
behavior of the ticket list.

    .value 'ticketFilterValues',

These values control the pagination. The value itemsPerPage is a constant.
TODO

        paginationBegin: 0,
        itemsPerPage: 3 // TODO

These are the initial values for the checkboxes and the search/filter input
field.

        remainingTime: false,
        closed: false // TODO
        search: ''


### Factory for ticket list header

Append a factory recipe with a Header constructor.

    .factory 'ticketListHeaderFactory', [
        ->
            Header: class
                constructor: (sortKey, displayName, col, icon) ->
                    @sortKey = sortKey
                    @displayName = displayName
                    @col = 'col-sm-' + col
                    @iconCSSClass = 'glyphicon-' + icon
    ]


### Factory for ticket list body

Append a factory recipe to return all tickets loaded from the backend. TODO

    .factory 'ticketListBodyFactory', [
        ->
            tickets: [
                    id: 1
                    content: 'Hallo'
                    status: 'New'
                    priority: 4
                    assignee: 'Dr. Berend Koll'
                    periodOrDeadline: 120
                ,
                    id: 2
                    content: 'AHallo ihr da mit dem wichtigen Text dort drüben.'
                    status: 'Closed'
                    priority: 1
                    assignee: 'Professor Dr. Christoph Enders'
                    periodOrDeadline: 42
                ,
                    id: 3
                    content: 'Kurzer Text ...'
                    status: 'Assigned'
                    priority: 5
                    assignee: 'Max'
                    periodOrDeadline: -12
                ,
                    id: 4
                    content: 'Kurzer MittelText ...'
                    status: 'Assigned'
                    priority: 2
                    assignee: 'Maxi'
                    periodOrDeadline: -11
            ]


    ]


## Controllers

### Controller for navigation bar at the top of the page

Append a controller for the top navigation bar.

    .controller 'NavbarCtrl', [
        'userHasPermissionFactory'
        class
            constructor: (@userHasPermissionFactory) ->
            userIsStaff: @userHasPermissionFactory.isStaff

    ]


### Controller for connection message

Append a controller for the message about the established connection short
after the top navigation bar.

    .controller 'ConnectionMessageCtrl', [
        class
            connectionOpen: true
    ]


### Controller for pagination bar

Append a controller for the pagination bar from angular-ui-bootstrap.

    .controller 'PaginationCtrl', [
        'ticketFilterValues'
        'ticketListBodyFactory'
        class
            constructor: (@ticketFilterValues, @ticketListBodyFactory) ->
            totalItems: @ticketListBodyFactory.tickets.length
            itemsPerPage: @ticketFilterValues.itemsPerPage
            change: =>
                @ticketFilterValues.paginationBegin = (@.paginationPage - 1) * @.itemsPerPage
                return
    ]


### Controller for the top row

Appends a controller for the row with the new button, the checkboxes and
the search bar.

    .controller 'TopRowCtrl', [
        'userHasPermissionFactory'
        'ticketFilterValues'
        class
            constructor: (@userHasPermissionFactory, @ticketFilterValues) ->

            newTicketForm: if @userHasPermissionFactory.canAddTicket then -> else null

            remainingTimeValue: @ticketFilterValues.remainingTime
            remainingTimeChange: =>
                @ticketFilterValues.remainingTime = @remainingTimeValue
                return

            closedValue: @ticketFilterValues.closed
            closedChange: =>
                @ticketFilterValues.closed = @closedValue
                return

            searchValue: @ticketFilterValues.search
            searchChange: =>
                @ticketFilterValues.search = @searchValue
                return
    ]

A second controller just to show another syntax.

    .controller 'TopRowCtrl2', [
        'userHasPermissionFactory'
        'ticketFilterValues'
        (userHasPermissionFactory, ticketFilterValues) ->
            @newTicketForm = if userHasPermissionFactory.canAddTicket then -> else null

            @remainingTimeValue = ticketFilterValues.remainingTime
            @remainingTimeChange = =>
                ticketFilterValues.remainingTime = @remainingTimeValue
                return

            @closedValue = ticketFilterValues.closed
            @closedChange = =>
                ticketFilterValues.closed = @closedValue
                return

            @searchValue = ticketFilterValues.search
            @searchChange = =>
                ticketFilterValues.search = @searchValue
                return
    ]


