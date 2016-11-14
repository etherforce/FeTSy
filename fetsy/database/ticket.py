from asyncio import coroutine

from .viewset import ObjectViewSet


class Ticket(ObjectViewSet):
    name = 'Ticket'
    uri_prefix = 'org.fetsy'
    new_object_timestamp = True
    new_object_schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": "New ticket",
        "description": "A new ticket without ID",
        "type": "object",
        "properties": {
            "content": {
                "description": "The content of the ticket",
                "type": "string"
            },
            "period": {
                "description": "The period in which the ticket has to be "
                               "solved",
                "type": "integer"
            }
        },
        "additionalProperties": False,
        "required": ["content"]
    }
    update_object_schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": "Changed ticket",
        "description": "A subset of a ticket to be changed",
        "type": "object",
        "properties": {
            "id": {
                "description": "The ID of the ticket",
                "type": "integer"
            },
            "content": {
                "description": "The content of the ticket",
                "type": "string"
            },
            "tags": {
                "description": "A list of ids refering to tags for this "
                               "ticket.",
                "type": "array",
                "items": {
                    "type": "integer",
                    "minimum": 1
                },
                "uniqueItems": True
            },
            "status": {
                "description": "The status of the ticket",
                "type": "string",
                "enum": [
                    "New",
                    "Work in progress",
                    "Closed"
                ]
            },
            "priority": {
                "description": "The priority of the ticket from low (1) to "
                               "high (5)",
                "type": "integer",
                "minimum": 1,
                "maximun": 5
            },
            "assignee": {
                "description": "The person who is resposible to solved the "
                               "ticket",
                "type": "string",
                "minLength": 1
            },
            "period": {
                "description": "The period in which the ticket has to be "
                               "solved",
                "type": "integer"
            }
        },
        "additionalProperties": False,
        "required": ["id"]
    }

    @coroutine
    def register_viewset(self):
        """
        Registeres all default procedures for this viewset. Additionally
        registeres list_ticket_assignees procedure.
        """
        yield from super().register_viewset()
        yield from self.app_session.register(
            self.list_ticket_assignees,
            self.uri_prefix + '.listTicketAssignees')
        self.logger.debug('Remote procedure to list Ticket assignees '
                          'registered.')

    def set_defaults(self, obj):
        """
        Set defaults for new tickets.
        """
        obj.setdefault('period', 120)
        obj['status'] = 'New'
        obj['priority'] = 3
        obj['assignee'] = '–'
        return obj

    @coroutine
    def list_ticket_assignees(self, *args, **kwargs):
        """
        Async method to get all assignees of all tickets.
        """
        self.logger.debug('Remote procedure list_ticket_assignees called.')
        curser = self.database[self.name].find()
        # TODO: For use of Mongo >= 3.2. Use $text operator.
        assignees = set()
        while (yield from curser.fetch_next):
            ticket = curser.next_object()
            assignees.add(ticket.get('assignee', ''))
        result = [assignee for assignee in assignees
                  if kwargs.get('filterValue', '').lower() in assignee.lower()]
        return result
