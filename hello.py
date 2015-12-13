import random
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationRunner, ApplicationSession


def returnlistOfTickets(*args, **kwargs):
    return [
        {
            'id': 1,
            'content': 'Hallo',
            'status': 'New',
            'priority': 4,
            'assignee': 'Dr. Berend Koll',
            'periodOrDeadline': 120,
        },
        {
            'id': 2,
            'content': 'AHallo ihr da mit dem wichtigen Text dort drüben.',
            'status': 'Closed',
            'priority': 1,
            'assignee': 'Professor Dr. Christoph Enders',
            'periodOrDeadline': 42,
        },
        {
            'id': 3,
            'content': 'Kurzer Text ...',
            'status': 'Assigned',
            'priority': 5,
            'assignee': 'Max',
            'periodOrDeadline': -12,
        },
        {
            'id': 4,
            'content': 'KKKKKurzer MittelText ...',
            'status': 'Assigned',
            'priority': 2,
            'assignee': 'Maxi',
            'periodOrDeadline': -11,
        }
    ]






class MyComponent(ApplicationSession):
    @coroutine
    def onJoin(self, details):
        yield from self.register(returnlistOfTickets, 'org.fetsy.listTickets')

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
    runner = ApplicationRunner(url='ws://localhost:8080/ws', realm='realm1')
    runner.run(MyComponent)
