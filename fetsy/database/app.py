"""
FeTSy database

This is a WAMP client application using MongoDB to store ticket data.
"""
import logging
from asyncio import coroutine

from autobahn.asyncio.wamp import ApplicationRunner, ApplicationSession
from motor.motor_asyncio import AsyncIOMotorClient

from .ticket import Ticket


class AppSession(Ticket, ApplicationSession):

    @coroutine
    def onJoin(self, details):
        # Take forwarded extra configuration.
        self.logger = self.config.extra['logger']
        self.logger.info('Connection to WAMP router established.')
        self.database = self.config.extra['database']
        yield from super().onJoin(details)


def main():
    """
    Main entry point for the database app.
    """
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
