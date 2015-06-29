/*!
 * JavaScript for FeTSy
 * Copyright (c) 2015 Norman Jäckel
 * Licensed under the MIT License
 */

(function () {

'use strict';

angular.module( 'FeTSy', [ 'FeTSyTicketControllers' ] )

// Set cookie and header name for CSRF Token (XSRF Token) to values expected
// by Django.
.config([ '$httpProvider', function ( $httpProvider ) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
} ]);

}());
