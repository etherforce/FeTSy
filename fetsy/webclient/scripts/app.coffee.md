# Base file for FeTSy AngularJS app

Initiate new angular module with the name 'FeTSy'. Load external libraries
(angular-moment, AngularWAMP and JSData) as dependencies. Load internal
services and controllers as dependencies.

    angular.module 'FeTSy', [
        'angularMoment'
        'vxWamp'
        'js-data'
        'FeTSy.services'
        'FeTSy.controllers'
    ]


## Setup and open WAMP connection using AngularWAMP (vxWamp)

Configurate the WAMP connection. Use 'realm1' als realm.

    .config [
        '$wampProvider'
        ($wampProvider) ->
            $wampProvider.init
                url: 'ws://' + location.host + '/ws'
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


## Setup and load JSData ressource for tickets

Append a factory recipe to the app which keeps the tickets ressource
definitions.

    .factory 'Ticket', [
        '$uibModal'
        'DS'
        ($uibModal, DS) ->
            DS.defineResource
                name: 'Ticket'
                methods:
                    openInfo: ->
                        $uibModal.open
                            templateUrl: 'ticketInfo.html'
                            controller: 'TicketInfoCtrl as ticketInfo'
                            resolve:
                                ticket: @
                        return
    ]

Load the ressource during app loading and setup WAMP opening event listener
to get all tickets from server.

    .run [
        '$rootScope'
        '$wamp'
        'Ticket'
        ($rootScope, $wamp, Ticket) ->
            $rootScope.$on '$wamp.open', (event, info) ->

Subscribe to the channel for new and changed tickets. If a ticket comes in,
check ticket id and inject it into data store.

                info.session.subscribe 'org.fetsy.changedTicket',
                    (args, kwargs, details) ->
                        if kwargs.ticket.id?
                            Ticket.inject kwargs.ticket
                        else
                            console.error 'Received invalid data.',
                                'ID is missing. Received'
                                kwargs.ticket
                        return

Fetch all tickets from server via procedure call.

                info.session.call 'org.fetsy.listTickets'
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

                return
            return
    ]
