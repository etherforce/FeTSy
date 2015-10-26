# Base file for FeTSy AngularJS app

Initiate new angular module with the name 'FeTSy'. Load services and
controllers as dependencies.

    angular.module 'FeTSy', [
        'js-data'
        'FeTSy.services'
        'FeTSy.controllers'
    ]

## Configurate JSData (js-data).

This does nothing at the moment.

    .config [
        'DSProvider'
        (DSProvider) ->
            return
    ]

## Setup Ticket ressource

    .factory 'Ticket', [
        'DS'
        (DS) ->
            DS.defineResource 'Ticket'
    ]

    .run [
        'Ticket'
        (Ticket) ->


TODO Remove the following lines

            tickets = [
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
            Ticket.inject ticket for ticket in tickets

            return
    ]

## Setup WAMP connection

Open the connection during loading.

    .run [
        'Ticket'
        (Ticket) ->

Setup connection using AutobahnJS.

            connection = new autobahn.Connection(
                url: 'ws://' + location.host + '/ws'
                realm: 'realm1'
            )

Create opening hook and call 'org.fetsy.listTickets' to get all tickets
from the server.

            connection.onopen = (session, details) ->
                session.call 'org.fetsy.listTickets'
                .then (result) ->
                    console.log result
                    Ticket.inject ticket for ticket in result
                return

Open connection.

            connection.open()
            return
    ]
