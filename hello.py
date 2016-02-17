import random
from asyncio import async, coroutine
from autobahn.asyncio.wamp import ApplicationRunner, ApplicationSession
from motor.motor_asyncio import AsyncIOMotorClient



def listOfTickets(database):

    @coroutine
    def mycoro():
        curser = database.tickets.find()
        tickets = yield from curser.to_list(length=100)
        print(tickets)
        return tickets


    def returnlistOfTickets(*args, **kwargs):
        coro = mycoro()
        async(coro)
        return ['sdf']

    return returnlistOfTickets





class MyComponent(ApplicationSession):
    @coroutine
    def onJoin(self, details):

        database = self.config.extra['database']

        yield from self.register(listOfTickets(database), 'org.fetsy.listTickets')

        def newTicket(*args, **kwargs):
            example_data = {
                    'id': random.choice([1, 2, 100, 101, None]),
                    'content': 'Text vom Server ' + random.choice('qwertzuioplkjhgfdsayxcvbnmMNBVCXYASDFGHJKLOIUZTREWQ'),
                    'status': 'Assigned',
                    'priority': 2,
                    'assignee': 'Maxi',
                    'periodOrDeadline': -11,
                }
            self.publish('org.fetsy.changedTicket', [4,5,6], ticket=example_data)

        yield from self.register(newTicket, 'org.fetsy.newTicket')
        # yield from self.register(...)


if __name__ == '__main__':
    client = AsyncIOMotorClient()
    database = client.fetsy
    runner = ApplicationRunner(
        url='ws://localhost:8080/ws',
        realm='realm1',
        extra={'database': database})
    runner.run(MyComponent)
