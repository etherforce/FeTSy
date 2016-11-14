# Base file for FeTSy directives

Initiate new angular module with the name 'FeTSy.directives'.

    angular.module 'FeTSy.directives', [
    ]


## Directive for field in the ticket list/ticket table

Append a directive which is used for every field of a ticket in the ticket
list/ticket table.

    .directive 'ticketField', [
        'Tag'
        (Tag) ->

Properties for the isolate scope binding.

            scope:
                ticket: '='
                key: '='

Controller for the field. The getTemplateURL() method returns different
URLs for each field. In some cases if the user clicks on a dropdown field
or hits Enter, the ticket is changed using a resource method.

            controller: [
                ->
                    @save = (value) ->
                        data = {}
                        data[@key] = value
                        @ticket.change data
                        .then =>
                            @editMode = false
                            return
                        return

                    @closeForm = ->
                        @inputField = @ticket.getField @key
                        @editMode = false
                        return

                    switch @key
                        when 'content'
                            @templateURL = 'ticketFieldTextarea.html'
                            @tags = Tag.filter
                                orderBy: 'weight'
                            @submitContentChanges = (content, tags) ->
                                data =
                                    content: content
                                    tags: tag.id for tag in tags
                                @ticket.change data
                                .then =>
                                    @editMode = false
                                    return
                                return
                        when 'status'
                            @templateURL = 'ticketFieldDropdown.html'
                            @dropdownChoices = [
                                'New'
                                'Work in progress'
                                'Closed'
                            ]
                        when 'priority'
                            @templateURL = 'ticketFieldDropdown.html'
                            @dropdownChoices = [1..5]
                        when 'assignee'
                            @templateURL = 'ticketFieldTypeahead.html'
                            @dropdownChoices = (value) =>
                                @ticket.getAssignees value
                                .then (result) ->
                                    result
                        else
                            @templateURL = 'ticketField.html'

                    return
            ]
            controllerAs: 'ticketField'
            bindToController: true

The template is just a ngInclude to fetch the template returned by
getTemplateURL().

            template: '<div ng-include="ticketField.templateURL"></div>'
    ]
