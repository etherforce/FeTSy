"""
FeTSy database

This is a WAMP client application using MongoDB to store ticket data.
"""
import datetime
import logging
from asyncio import Lock, coroutine

from autobahn.asyncio.wamp import ApplicationRunner, ApplicationSession
from jsonschema import ValidationError, validate
from motor.motor_asyncio import AsyncIOMotorClient

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

new_ticket_lock = Lock()


class AppSession(ApplicationSession):

    @coroutine
    def onJoin(self, details):
        # Take forwarded extra configuration.
        self.logger = self.config.extra['logger']
        self.logger.info('Connection to WAMP router established.')
        self.database = self.config.extra['database']

        # Register remote procedures.
        yield from self.register(self.list_tickets, 'org.fetsy.listTickets')
        yield from self.register(self.new_ticket, 'org.fetsy.newTicket')
        yield from self.register(self.change_ticket, 'org.fetsy.changeTicket')

    @coroutine
    def list_tickets(self, *args, **kwargs):
        self.logger.debug('Remote procedure list_tickets called.')
        curser = self.database.tickets.find()
        tickets = []
        while (yield from curser.fetch_next):
            ticket = curser.next_object()
            del ticket['_id']
            tickets.append(ticket)
        return tickets

    @coroutine
    def new_ticket(self, *args, **kwargs):
        """
        Async method to create new tickets in the database.
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
        ticket['assignee'] = 'Max'
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
            # For use of Mongo >= 2.5
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

    @coroutine
    def change_ticket(self, *args, **kwargs):
        """
        Async method to change tickets in the database.
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


if __name__ == '__main__':
    # Setup logging.
    logging.info('Entering main entry point.')
    logger = logging.getLogger(__file__)
    logger.setLevel(logging.DEBUG)

    # Setup database connection.
    client = AsyncIOMotorClient()
    database = client.fetsy

    # Setup and run application.
    runner = ApplicationRunner(
        url='ws://localhost:8080/ws',
        realm='realm1',
        extra={
            'database': database,
            'logger': logger})
    runner.run(AppSession)
