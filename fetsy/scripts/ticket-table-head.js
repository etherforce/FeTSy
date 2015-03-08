(function () {

'use strict';

angular.module( 'FeTSyTicketTableHead', [] )

// Factory to setup ticket table headers with sort functionality and also
// search bar and checkbox.
.factory( 'setupTableSearchAndSort' , function () {
    return function ( ticketCtrl ) {
        // Define table headers.
        ticketCtrl.headers = [
            { 'key': 'id' },
            { 'key': 'content', 'verboseName': 'Content', 'cssIconClass': 'glyphicon-cog' },
            { 'key': 'status', 'verboseName': 'Status', 'cssIconClass': 'glyphicon-star' },
            { 'key': 'priority', 'verboseName': 'Priority', 'cssIconClass': 'glyphicon-fire' },
            { 'key': 'assignee.name', 'verboseName': 'Assignee', 'cssIconClass': 'glyphicon-user' },
            { 'key': 'timeToEnd', 'verboseName': 'Remaining time', 'cssIconClass': 'glyphicon-hourglass' }
        ];

        // Setup table filtering using the checkboxes and the search filter.
        ticketCtrl.search = undefined;
        ticketCtrl.showClosed = false;
        ticketCtrl.closedFilter = function ( value, index ) {
            return ticketCtrl.showClosed || value.status !== 'Closed';
        };

        // Setup table sorting
        ticketCtrl.sortColumn = ticketCtrl.headers[0].key;
        ticketCtrl.reverse = true;
        ticketCtrl.toggleSort = function ( index ) {
            if ( ticketCtrl.sortColumn === ticketCtrl.headers[index].key ) {
                ticketCtrl.reverse = !ticketCtrl.reverse;
            }
            ticketCtrl.sortColumn = ticketCtrl.headers[index].key;
        };
    };
});

}());
