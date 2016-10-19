# Base file for FeTSy AngularJS app

Initiate new angular module with the name 'FeTSy'. Load external libraries
(angular-moment, AngularWAMP, JSData and UI-Router for Angular 1) as
dependencies. Load internal services, controllers and directives as
dependencies.

    angular.module 'FeTSy', [
        'angularMoment'
        'vxWamp'
        'js-data'
        'ui.router'
        'FeTSy-templates'
        'FeTSy.services'
        'FeTSy.controllers'
        'FeTSy.directives'
    ]


## Configurate UI-Router for Angular 1 (ui.rooter).

    .config [
        '$locationProvider'
        '$urlRouterProvider'
        ($locationProvider, $urlRouterProvider) ->

            # Uses HTML5 mode for location in browser address bar
            $locationProvider.html5Mode true

            # For any unmatched url, redirect to /
            $urlRouterProvider.otherwise '/'
    ]

    .config [
        '$stateProvider'
        ($stateProvider) ->
            $stateProvider
            .state
                name: 'home'
                url: '/'
                templateUrl: 'home.html'
            .state
                name: 'administration'
                url: '/administration/'
                templateUrl: 'administration.html'
            return
    ]


## Setup and open WAMP connection using AngularWAMP (vxWamp)

Configurate the WAMP connection. Use 'realm1' als realm.

    .config [
        '$wampProvider'
        ($wampProvider) ->
            $wampProvider.init
                url: "ws://#{ location.host }/ws"
                realm: 'realm1'
            return
    ]

Open WAMP connection during app loading.

    .run [
        '$wamp'
        ($wamp) ->
            $wamp.open()
            return
    ]


## Configurate JSData (js-data).

This does nothing at the moment. TODO: Remove this stuff.

    .config [
        'DSProvider'
        (DSProvider) ->
            return
    ]


## Setup and load JSData ressource for tickets and tags

Append a factory recipe to the app which keeps the tickets ressource
definitions.

    .factory 'Ticket', [
        '$uibModal'
        '$wamp'
        'DS'
        'ticketFilterValues'
        'contentLimit'
        ($uibModal, $wamp, DS, ticketFilterValues, contentLimit) ->
            DS.defineResource
                name: 'Ticket'
                methods:

The method 'getField' returns the value of the ticket field. In case of
'content' the text is possibly limited to the value of the 'contentLimit'
constant. In case of 'period' the result depends on the flag
'remainingTime'.

                    getField: (key) ->
                        if key is 'content' and @content.length > contentLimit
                            @content.slice(0, contentLimit) + '...'
                        else if key is 'period'
                            momentDeadline = moment.unix @created
                                .add @period, 'minutes'
                            if 0 > momentDeadline.diff moment(), 'minutes'
                                @expired = true
                            if ticketFilterValues.remainingTime
                                String(
                                    momentDeadline.diff moment(), 'minutes'
                                ) + ' min.'
                            else
                                if momentDeadline.isSame moment(), 'day'
                                    'Today' + ' ' + momentDeadline.format 'HH:mm'
                                else if momentDeadline.isSame moment().add(1, 'day'), 'day'
                                    'Tomorrow' + ' ' + momentDeadline.format 'HH:mm'
                                else
                                    momentDeadline.format 'YYYY-MM-DD HH:mm'
                        else
                            @[key]

The method 'getAssignees' fetches an array of all assignees of all tickets.
It returns a promise which is resolved with this array.

                    getAssignees: (filterValue) ->
                        $wamp.call 'org.fetsy.listTicketAssignees', [],
                            filterValue: filterValue
                        .then (result) ->
                            if typeof result is 'object'
                                result
                            else
                                console.error 'Received invalid data.',
                                    'List of assignees is missing. Received'
                                    result
                                []

The method 'openInfo' opens a modal with more info about the ticket.

                    openInfo: ->
                        $uibModal.open
                            templateUrl: 'ticketInfo.html'
                            controller: 'TicketInfoCtrl as ticketInfo'
                            resolve:
                                ticket: @
                        return

The method 'change' requests the server to change the data of the ticket.
It returns a promise.

                    change: (data) ->
                        data.id = @id
                        $wamp.call 'org.fetsy.updateTicket', [],
                            object: data
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
    ]

Append a factory recipe to the app which keeps the tags ressource definitions.

    .factory 'Tag', [
        'DS'
        (DS) ->
            DS.defineResource
                name: 'Tag'
    ]

Load the ressource during app loading and setup WAMP opening event listener
to get all tickets and tags from server.

    .run [
        '$rootScope'
        '$wamp'
        'Ticket'
        'Tag'
        ($rootScope, $wamp, Ticket, Tag) ->
            $rootScope.$on '$wamp.open', (event, info) ->

Subscribe to the channel for new and changed tickets. If a ticket comes in,
check ticket id and inject it into data store.

                info.session.subscribe 'org.fetsy.changedTicket',
                    (args, kwargs, details) ->
                        if kwargs.object.id?
                            Ticket.inject kwargs.object
                        else
                            console.error 'Received invalid data.',
                                'ID is missing. Received'
                                kwargs.object
                        return

Subscribe to the channel for deleted tickets. If an id comes in, eject the
ticket out of data store.

                info.session.subscribe 'org.fetsy.deletedTicket',
                    (args, kwargs, details) ->
                        if kwargs.id?
                            Ticket.eject kwargs.id
                        else
                            console.error 'Received invalid data.',
                                'ID is missing. Received'
                                kwargs
                        return

Subscribe to the channel for new and changed tags. If a tag comes in,
check tag id and inject it into data store.

                info.session.subscribe 'org.fetsy.changedTag',
                    (args, kwargs, details) ->
                        if kwargs.object.id?
                            Tag.inject kwargs.object
                        else
                            console.error 'Received invalid data.',
                                'ID is missing. Received'
                                kwargs.object
                        return

Fetch all tickets from server via procedure call.

                info.session.call 'org.fetsy.listTicket'
                    .then (result) ->
                        for item in result
                            if item.id?
                                ticket = Ticket.get item.id
                                if ticket?
                                    angular.extend item, ticket
                                Ticket.inject item
                            else
                                console.error 'Received invalid data.',
                                    'ID is missing. Received'
                                    item
                        return

Fetch all tags from server via procedure call.

                info.session.call 'org.fetsy.listTag'
                    .then (result) ->
                        for item in result
                            if item.id?
                                tag = Tag.get item.id
                                if tag?
                                    angular.extend item, tag
                                Tag.inject item
                            else
                                console.error 'Received invalid data.',
                                    'ID is missing. Received'
                                    item
                        return

                return
            return
    ]
