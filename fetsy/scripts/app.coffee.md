# Base file for FeTSy AngularJS app

Initiate new angular module with the name 'FeTSy'. Load services and
controllers as dependencies.

    angular.module 'FeTSy', [
        'js-data'
        'FeTSy.services'
        'FeTSy.controllers'
    ]

## Register our WAMP adapter.

    .service 'FetsyWAMPAdapter', [
        () ->
            return
    ]

## Configurate JSData (js-data) Part 1

    .config [
        'DSProvider'
        (DSProvider) ->
            angular.extend DSProvider.defaults, basePath: '/baseurl'
            return
    ]

## Setup Ticket ressource

    .factory 'Ticket', [
        'DS'
        (DS) ->
            DS.defineResource 'Ticket'
    ]

## Configurate JSData (js-data) Part 2

    .run [
        'DS'
        'FetsyWAMPAdapter'
        'Ticket'
        (DS, FetsyWAMPAdapter, Ticket) ->
            # DS.registerAdapter 'wamp', FetsyWAMPAdapter, default: true

            Ticket.findAll()
            return
    ]
