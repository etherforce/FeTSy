"""
FeTSy database

This is a WAMP client application using MongoDB to store ticket data.
"""
import logging
import random
from asyncio import coroutine

from autobahn.asyncio.wamp import ApplicationRunner, ApplicationSession
from motor.motor_asyncio import AsyncIOMotorClient


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
        # yield from self.subscribe(self.changedTicket, 'org.fetsy.changedTicket')

    @coroutine
    def list_tickets(self, *args, **kwargs):
        self.logger.debug('Remote procedure list_tickets was called.')
        curser = self.database.tickets.find()
        tickets = []
        while (yield from curser.fetch_next):
            ticket = curser.next_object()
            del ticket['_id']
            tickets.append(ticket)
        self.logger.debug(tickets)
        return tickets

    @coroutine
    def new_ticket(self, *args, **kwargs):
        # TODO: Take data from client instead of example data.
        ticket = {
                'content': 'Text vom Server ' + random.choice('qwertzuioplkjhgfdsayxcvbnmMNBVCXYASDFGHJKLOIUZTREWQ'),
                'status': 'Assigned',
                'priority': 2,
                'assignee': 'Maxi',
                'periodOrDeadline': -11}

        # Fetch biggest ID from database.
        max_id_key = 'maxID'
        pipeline = [
            {'$sort': {'id': 1}},
            {'$group': {'_id': None, max_id_key: {'$last': '$id'}}}]
        future_result = yield from self.database.tickets.aggregate(pipeline, cursor=False)
        self.logger.debug(future_result)
        if future_result['result']:
            max_id = future_result['result'][0][max_id_key]
        else:
            max_id = 0
        # curser = self.database.tickets.aggregate(pipeline)  # For use of Mongo >= 2.5
        # while (yield from curser.fetch_next):
        #    result = curser.next_object()

        # Insert new ticket to database.
        ticket['id'] = max_id + 1
        yield from self.database.tickets.insert(ticket)
        del ticket['_id']

        # Publish changedTicket event.
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
