# Base file for FeTSy directives

Initiate new angular module with the name 'FeTSy.directives'.

    angular.module 'FeTSy.directives', [
    ]


## Directive for field in the ticket list/ticket table

Append a directive which is used for every field of a ticket in the ticket
list/ticket table.

    .directive 'ticketField', [
        ->

Properties for the isolate scope binding.

            scope:
                ticket: '='
                key: '='

Controller for the field. The getTemplateURL() method returns different
URLs for each field. This depends on the result of getDropdownChoices().

            controller: [
                '$scope'
                ($scope) ->
                    @ticket = $scope.ticket
                    @key = $scope.key
                    @getDropdownChoices = ->
                        switch $scope.key
                            when 'status' then [
                                'New'
                                'Work in progress'
                                'Closed'
                            ]
                            when 'assignee' then [
                                'v'
                            ]
                            when 'priority' then [
                                1
                                2
                                3
                                4
                                5
                            ]
                            else null
                    @getTemplateURL = ->
                        if @getDropdownChoices()
                            'ticketFieldDropdown.html'
                        else
                            'ticketField.html'
                    @click = (choice) ->
                        console.log choice
                        console.log @key
                        return
                    return
            ]
            controllerAs: 'ticketField'

The template is just a ngInclude to fetch the template returned by
getTemplateURL().

            template: '<div ng-include="ticketField.getTemplateURL()"></div>'
    ]
