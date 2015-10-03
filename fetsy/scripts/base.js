(function () {

    angular.module('FeTSy', ['ui.bootstrap'])

    .factory('userHasPermissionFactory', [
        function () {
            return {
                canAddTicket: true,
                canChangeTicket: true,
                isStaff: true
            };
        }
    ])

    .value('ticketFilterValues', {
        paginationBegin: 0,
        itemsPerPage: 3, // TODO
        remainingTime: false,
        closed: false, // TODO
        search: '',
    })

    .factory('ticketListHeaderFactory', [
        function () {
            return {
                Header: function (sortKey, displayName, col, icon) {
                    this.sortKey = sortKey;
                    this.displayName = displayName;
                    this.col = 'col-sm-' + col;
                    this.iconCSSClass = 'glyphicon-' + icon;
                }
            };
        }
    ])

    .factory('ticketListBodyFactory', [
        function () {
            return {
                tickets: [
                    {
                        id: 1,
                        content: 'Hallo',
                        status: 'New',
                        priority: 4,
                        assignee: 'Dr. Berend Koll',
                        periodOrDeadline: 120
                    },
                    {
                        id: 2,
                        content: 'AHallo ihr da mit dem wichtigen Text dort drüben.',
                        status: 'Closed',
                        priority: 1,
                        assignee: 'Professor Dr. Christoph Enders',
                        periodOrDeadline: 42
                    },
                    {
                        id: 3,
                        content: 'Kurzer Text ...',
                        status: 'Assigned',
                        priority: 5,
                        assignee: 'Max',
                        periodOrDeadline: -12
                    },
                    {
                        id: 4,
                        content: 'Kurzer MittelText ...',
                        status: 'Assigned',
                        priority: 2,
                        assignee: 'Maxi',
                        periodOrDeadline: -11
                    }
                ]
            };
        }
    ])

    .controller('NavbarCtrl', [
        'userHasPermissionFactory',
        function (userHasPermissionFactory) {
            this.userIsStaff = userHasPermissionFactory.isStaff;
        }
    ])

    .controller('ConnectionMessageCtrl', [
        function () {
            this.connectionOpen = true;
        }
    ])

    .controller('PaginationCtrl', [
        'ticketFilterValues',
        'ticketListBodyFactory',
        function (ticketFilterValues, ticketListBodyFactory) {
            this.totalItems = ticketListBodyFactory.tickets.length;
            this.itemsPerPage = ticketFilterValues.itemsPerPage;
            this.change = function () {
                ticketFilterValues.paginationBegin = (this.paginationPage - 1) * this.itemsPerPage;
            };
        }
    ])

    .controller('TopRowCtrl', [
        'userHasPermissionFactory',
        'ticketFilterValues',
        function (userHasPermissionFactory, ticketFilterValues) {
            var topRow = this;

            // New ticket button.
            topRow.newTicketForm = userHasPermissionFactory.canAddTicket ? function () {} : undefined;  // TODO

            // Show remaining time in minutes checkbox.
            topRow.remainingTimeValue = ticketFilterValues.remainingTime;
            topRow.remainingTimeChange = function () {
                ticketFilterValues.remainingTime = topRow.remainingTimeValue;
            };

            // Hide closed tickets checkbox.
            topRow.closedValue = ticketFilterValues.closed;
            topRow.closedChange = function () {
                ticketFilterValues.closed = topRow.closedValue;
            };

            // Search bar for filtering the table.
            topRow.searchValue = ticketFilterValues.search;
            topRow.searchChange = function () {
                ticketFilterValues.search = topRow.searchValue;
            };
        }
    ])

    .controller('TicketListCtrl', [
        'ticketFilterValues',
        'ticketListHeaderFactory',
        'ticketListBodyFactory',
        function (ticketFilterValues, ticketListHeaderFactory, ticketListBodyFactory) {
            var tickets = this;

            // Pagination bar and top functionality row.
            tickets.itemsPerPage = ticketFilterValues.itemsPerPage;
            tickets.getPaginationBegin = function () {
                return ticketFilterValues.paginationBegin;
            };
            tickets.getSearch = function () {
                return ticketFilterValues.search;
            };
            tickets.closedFilter = function (value, index) {
                return !ticketFilterValues.closed || value.status !== 'Closed';
            };

            // Ticket list header with initial values.
            tickets.headers = [
                new ticketListHeaderFactory.Header('id', 'Number', '1'),
                new ticketListHeaderFactory.Header('content', 'Content', '4', 'cog'),
                new ticketListHeaderFactory.Header('status', 'Status', '1', 'star'),
                new ticketListHeaderFactory.Header('priority', 'Priority', '1', 'fire'),
                new ticketListHeaderFactory.Header('assignee', 'Assignee', '2', 'user'),
                new ticketListHeaderFactory.Header('periodOrDeadline', 'Period or deadline', '2', 'hourglass'),  // 'time'
            ];
            tickets.sortColumn = 'id';
            tickets.reverse = true;
            tickets.toggleSort = function (sortKey) {
                if (tickets.sortColumn === sortKey) {
                    tickets.reverse = !tickets.reverse;
                } else {
                    tickets.sortColumn = sortKey;
                }
            };

            // Ticket list body.
            tickets.all = ticketListBodyFactory.tickets;
        }
    ]);

}());
