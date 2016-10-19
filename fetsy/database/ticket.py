import datetime

from asyncio import Lock, coroutine
from jsonschema import ValidationError, validate

from .viewset import ObjectViewSet

new_ticket_lock = Lock()

new_ticket_schema = {
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
            "description": "The period in which the ticket has to be solved",
            "type": "integer"
        }
    },
    "additionalProperties": False,
    "required": ["content"]
}

changed_ticket_schema = {
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
            "description": "The person who is resposible to solved the ticket",
            "type": "string"
        },
        "period": {
            "description": "The period in which the ticket has to be solved",
            "type": "integer"
        }
    },
    "additionalProperties": False,
    "required": ["id"]
}


class Ticket2(ObjectViewSet):
    name='Ticket'
    uri_prefix = 'org.fetsy'
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
                "description": "The period in which the ticket has to be solved",
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
                "description": "The person who is resposible to solved the ticket",
                "type": "string"
            },
            "period": {
                "description": "The period in which the ticket has to be solved",
                "type": "integer"
            }
        },
        "additionalProperties": False,
        "required": ["id"]
    }


class ListTicket:
    """
    Interactions to list some or all tickets.
    """
    @coroutine
    def onJoin(self, details):
        yield from self.register(self.list_tickets, 'org.fetsy.listTickets')
        next_method = super().onJoin(details)
        if next_method is not None:
            yield from next_method

    @coroutine
    def list_tickets(self, *args, **kwargs):
        """
        Async method to get some tickets from the database.
        """
        # TODO: Use filtering here.
        self.logger.debug('Remote procedure list_tickets called.')
        curser = self.database.tickets.find()
        tickets = []
        while (yield from curser.fetch_next):
            ticket = curser.next_object()
            del ticket['_id']
            tickets.append(ticket)
        return tickets


class CreateTicket:
    """
    Interactions to create a new ticket.
    """
    @coroutine
    def onJoin(self, details):
        yield from self.register(self.new_ticket, 'org.fetsy.newTicket')
        next_method = super().onJoin(details)
        if next_method is not None:
            yield from next_method

    @coroutine
    def new_ticket(self, *args, **kwargs):
        """
        Async method to create a new ticket in the database.
        """
        self.logger.debug('Remote procedure new_ticket called.')
        try:
            ticket = self.validate_new_ticket(kwargs.get('ticket'))
        except ValidationError as e:
            result = {
                'type': 'error',
                'details': e.message}
        else:
            yield from self.save_new_ticket(ticket)
            success = 'Ticket {} successfully created.'.format(ticket['id'])
            result = {
                'type': 'success',
                'details': success}
        return result

    def validate_new_ticket(self, ticket):
        """
        Validates data for new tickets and adds default values.
        """
        if ticket is None:
            raise ValidationError('Ticket data is missing')
        validate(ticket, new_ticket_schema)
        ticket.setdefault('period', 120)
        ticket['status'] = 'New'
        ticket['priority'] = 3
        ticket['assignee'] = 'Max'  # TODO: Use Nobody here.
        return ticket

    @coroutine
    def save_new_ticket(self, ticket):
        """
        Async method to store a new ticket in the database. Adds a new 'id'
        property.
        """
        with (yield from new_ticket_lock):
            # Fetch biggest ID from database.
            max_id_key = 'maxID'
            pipeline = [
                {'$sort': {'id': 1}},
                {'$group': {'_id': None, max_id_key: {'$last': '$id'}}}]
            future_result = yield from self.database.tickets.aggregate(
                pipeline, cursor=False)
            if future_result['result']:
                max_id = future_result['result'][0][max_id_key]
            else:
                max_id = 0
            # TODO: For use of Mongo >= 2.5
            # curser = self.database.tickets.aggregate(pipeline)
            # while (yield from curser.fetch_next):
            #    result = curser.next_object()

            # Insert new ticket in database. Add timestamp.
            ticket['id'] = max_id + 1
            ticket['created'] = datetime.datetime.now().timestamp()
            yield from self.database.tickets.insert(ticket)

        # Publish changedTicket event.
        del ticket['_id']
        self.publish('org.fetsy.changedTicket', [], ticket=ticket)


class UpdateTicket:
    """
    Interactions to change a ticket.
    """
    @coroutine
    def onJoin(self, details):
        yield from self.register(self.change_ticket, 'org.fetsy.changeTicket')
        next_method = super().onJoin(details)
        if next_method is not None:
            yield from next_method

    @coroutine
    def change_ticket(self, *args, **kwargs):
        """
        Async method to change a ticket in the database.
        """
        self.logger.debug('Remote procedure change_ticket called.')
        try:
            ticket = self.validate_changed_ticket(kwargs.get('ticket'))
        except ValidationError as e:
            result = {
                'type': 'error',
                'details': e.message}
        else:
            yield from self.save_changed_ticket(ticket)
            success = 'Ticket {} successfully changed.'.format(ticket['id'])
            result = {
                'type': 'success',
                'details': success}
        return result

    def validate_changed_ticket(self, ticket):
        """
        Validates data for changed tickets.
        """
        if ticket is None:
            raise ValidationError('Ticket data is missing')
        validate(ticket, changed_ticket_schema)
        return ticket

    @coroutine
    def save_changed_ticket(self, ticket):
        """
        Async method to store changes of a ticket in the database.
        """
        yield from self.database.tickets.update(
            {'id': ticket['id']},
            {'$set': ticket}
        )
        self.publish('org.fetsy.changedTicket', [], ticket=ticket)


class DeleteTicket:
    """
    Interactions to delete a ticket.
    """
    @coroutine
    def onJoin(self, details):
        yield from self.register(self.delete_ticket, 'org.fetsy.deleteTicket')
        next_method = super().onJoin(details)
        if next_method is not None:
            yield from next_method

    @coroutine
    def delete_ticket(self, *args, **kwargs):
        """
        Async method to delete a ticket.
        """
        self.logger.debug('Remote procedure delete_ticket called.')
        id = kwargs.get('id')
        yield from self.database.tickets.remove({'id': id})
        self.publish('org.fetsy.deletedTicket', [], id=id)
        success = 'Ticket {} successfully deleted.'.format(id)
        return {
            'type': 'success',
            'details': success}


class MetadataTicket:
    """
    Interactions to retrieve metadata of tickests.

    This is only a list of all assignees at the moment.
    """
    @coroutine
    def onJoin(self, details):
        yield from self.register(
            self.list_ticket_assignees,
            'org.fetsy.listTicketAssignees')
        next_method = super().onJoin(details)
        if next_method is not None:
            yield from next_method

    @coroutine
    def list_ticket_assignees(self, *args, **kwargs):
        """
        Async method to get all assignees of all tickets.
        """
        self.logger.debug('Remote procedure list_ticket_assignees called.')
        curser = self.database.tickets.find()
        # TODO: For use of Mongo >= 3.2. Use $text operator.
        assignees = set()
        while (yield from curser.fetch_next):
            ticket = curser.next_object()
            assignees.add(ticket.get('assignee', ''))
        result = [assignee for assignee in assignees
                  if kwargs.get('filterValue', '').lower() in assignee.lower()]
        return result


class Ticket(ListTicket, CreateTicket, UpdateTicket, DeleteTicket,
             MetadataTicket):
    """
    Interactions for tickets.
    """
    pass
