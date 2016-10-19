"""
FeTSy database

This is a WAMP client application using MongoDB to store ticket data.
"""
import logging
from asyncio import coroutine

from autobahn.asyncio.wamp import ApplicationRunner, ApplicationSession
from motor.motor_asyncio import AsyncIOMotorClient

from .tag import Tag
from .ticket import Ticket


class AppSession(ApplicationSession):

    @coroutine
    def onJoin(self, details):
        # Take forwarded extra configuration.
        self.logger = self.config.extra['logger']
        self.logger.info('Connection to WAMP router established.')
        self.database = self.config.extra['database']

        # Register Ticket ViewSet.
        ticket = Ticket(self)  #TODO: Change name to Ticket.
        yield from ticket.register_viewset()

        # Register Tag ViewSet.
        tag = Tag(self)
        yield from tag.register_viewset()


def get_config():
    """
    Returns a dictionary with the configuration of this application.
    """
    host = 'localhost'
    port = '8080'
    return {
        'host': host,
        'port': port,
        'router_url': 'ws://{host}:{port}/ws'.format(host=host, port=port),
    }


def main():
    """
    Main entry point for the database app.
    """
    # Setup logging.
    logging.info('Entering main entry point.')
    logger = logging.getLogger(__file__)
    logger.setLevel(logging.DEBUG)

    # Get application configuration
    config = get_config()
    webclient_url = 'http://{host}:{port}/'.format(
        host=config['host'],
        port=config['port'])

    # Setup database connection.
    client = AsyncIOMotorClient()
    database = client.fetsy

    # Setup and run application.
    logger.info('Try to open webclient at {webclient_url}.'.format(
        webclient_url=webclient_url))
    runner = ApplicationRunner(
        url=config['router_url'],
        realm='realm1',
        extra={
            'database': database,
            'logger': logger})
    runner.run(AppSession)
