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
URLs for each field. In some cases if the user clicks on a dropdown field
or hits Enter, the ticket is changed using a resource method.

            controller: [
                '$scope'
                ($scope) ->
                    @ticket = $scope.ticket
                    @key = $scope.key
                    getNames = (value) =>
                        @ticket.getAssignees value
                        .then (result) ->
                            result
                    @getDropdownChoices = ->
                        switch @key
                            when 'status' then [
                                'New'
                                'Work in progress'
                                'Closed'
                            ]
                            when 'assignee' then getNames
                            when 'priority' then [1..5]
                            else null
                    @getTemplateURL = ->
                        switch @key
                            when 'status' then 'ticketFieldDropdown.html'
                            when 'priority' then 'ticketFieldDropdown.html'
                            when 'assignee' then 'ticketFieldTypeahead.html'
                            else 'ticketField.html'
                    @click = (choice) ->
                        data = {}
                        data[@key] = choice
                        @ticket.change data
                        .then =>
                            @editMode = false
                            return
                        return
                    @closeForm = ->
                        @inputField = @ticket.getField @key
                        @editMode = false
                        return
                    return
            ]
            controllerAs: 'ticketField'

The template is just a ngInclude to fetch the template returned by
getTemplateURL().

            template: '<div ng-include="ticketField.getTemplateURL()"></div>'
    ]
