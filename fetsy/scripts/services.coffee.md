# Base file for FeTSy services

Initiate new angular module with the name 'FeTSy.services'.

    angular.module 'FeTSy.services', []

Now setup some services (factory recipes, value recipes) we use.


## User's Permission factory

Append a factory recipe to the app which keeps the user's permissions. TODO

    .factory 'userHasPermissionFactory', [
        ->
            canAddTicket: true
            canChangeTicket: true
            isStaff: true
    ]


## Values for ticket list filtering

Append a value recipe to the app which stores values to controll the
behavior of the ticket list.

    .value 'ticketFilterValues',

These values control the pagination. The value itemsPerPage is a constant.
TODO itemsPerPage

        paginationBegin: 0
        itemsPerPage: 3

These are the initial values for the checkboxes and the search/filter input
field. TODO Set closed to true.

        remainingTime: false
        closed: false
        search: ''


## Factory for ticket list header

Append a factory recipe with a Header constructor.

    .factory 'ticketListHeaderFactory', [
        ->
            Header: class
                constructor: (options) ->
                    @sortKey = options.sortKey
                    @displayName = options.displayName
                    @col = 'col-sm-' + options.col
                    @iconCSSClass = 'glyphicon-' + options.icon
    ]
