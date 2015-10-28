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


def newTicket(*args, **kwargs):
    print('New Ticket')
    print(args)
    print(kwargs)


class MyComponent(ApplicationSession):
    @coroutine
    def onJoin(self, details):
        yield from self.register(returnlistOfTickets, 'org.fetsy.listTickets')
        yield from self.subscribe(newTicket, 'org.fetsy.newTicket')
        # yield from self.register(...)


if __name__ == '__main__':
    runner = ApplicationRunner(url='ws://localhost:8080/ws', realm='realm1')
    runner.run(MyComponent)
