# Base file for FeTSy services

Initiate new angular module with the name 'FeTSy.services'.
TODO: Rename this to 'FeTSy.providers'.

    angular.module 'FeTSy.services', []

Now setup some provider recipes (factory recipes, value recipes, constant
recipes) we use.


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
        itemsPerPage: 10

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
                    @col = 'col-sm-' + options.col
                    @getDisplayName = ->
                        if typeof options.displayName is 'function'
                            options.displayName()
                        else
                            options.displayName
                    @getIconCSSClass = ->
                        if typeof options.icon is 'function'
                            'glyphicon-' + options.icon()
                        else
                            'glyphicon-' + options.icon
    ]

## Constant for default period.

Append a constant for the default period. It is used in the new ticket form
modal.

    .constant 'defaultPeriod', 120


## Constant for the character limit in the content field.

Append a constant to set a limit of characters in the content field in the
ticket table. If a ticket has a longer content, the text is sliced.

    .constant 'contentLimit', 30
