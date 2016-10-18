import datetime

from asyncio import Lock, coroutine
from jsonschema import ValidationError, validate


class ListObjectsMixin:
    """
    Interactions to list some or all objects from the database.
    """
    @coroutine
    def register_viewset(self):
        """
        Registeres list_objects procedure.
        """
        yield from self.app_session.register(self.list_objects, self.get_uri('list'))
        self.logger.debug('Remote procedure to list {} registered.'.format(self.name))
        if hasattr(super(), 'register_viewset'):
            yield from super().register_viewset()

    @coroutine
    def list_objects(self, *args, **kwargs):
        """
        Async method to list some or all objects from the database.
        """
        # TODO: Use filtering here.
        self.logger.debug('Remote procedure list_objects for {} called.'.format(self.name))
        curser = self.database[self.name].find()
        objects = []
        while (yield from curser.fetch_next):
            obj = curser.next_object()
            del obj['_id']
            objects.append(obj)
        return objects


class CreateObjectsMixin:
    """
    Interactions to create a new object in the database.
    """
    new_object_schema = None
    new_object_timestamp = False

    def __init__(self):
        self.create_object_lock = Lock()
        return super().__init__()

    @coroutine
    def register_viewset(self):
        """
        Registeres create_object procedure.
        """
        yield from self.app_session.register(self.create_object, self.get_uri('create'))
        self.logger.debug('Remote procedure to create {} registered.'.format(self.name))
        if hasattr(super(), 'register_viewset'):
            yield from super().register_viewset()

    @coroutine
    def create_object(self, *args, **kwargs):
        """
        Async method to create a new object in the database.
        """
        self.logger.debug('Remote procedure create_object for {} called.'.format(self.name))
        try:
            obj = self.validate_new_object(kwargs.get('object'))
        except ValidationError as e:
            result = {
                'type': 'error',
                'details': e.message}
        else:
            # TODO: obj = self.set_defaults(obj)
            yield from self.save_new_object(obj)
            success = '{} object {} successfully created.'.format(self.name, obj['id'])
            result = {
                'type': 'success',
                'details': success}
        return result

    def validate_new_object(self, obj):
        """
        Validates data for new objects.
        """
        if self.new_object_schema is None:
            raise NotImplementedError('ViewSet new_object_schema is missing.')
        if obj is None:
            raise ValidationError('Object data is missing.')
        validate(obj, self.new_object_schema)
        return obj

    @coroutine
    def save_new_object(self, obj):
        """
        Async method to store a new object in the database. Adds a new 'id'
        property.
        """
        with (yield from self.create_object_lock):
            # Get greatest ID from database.
            max_id_key = 'maxID'
            pipeline = [
                {'$sort': {'id': 1}},
                {'$group': {'_id': None, max_id_key: {'$last': '$id'}}}]
            future_result = yield from self.database[self.name].aggregate(
                pipeline, cursor=False)
            if future_result['result']:
                max_id = future_result['result'][0][max_id_key]
            else:
                max_id = 0
            # TODO: When upgrading to MongoDB >= 2.5
            # curser = self.database[self.name].aggregate(pipeline)
            # while (yield from curser.fetch_next):
            #    result = curser.next_object()

            # Add timestamp if configured.
            if self.new_object_timestamp:
                obj['created'] = datetime.datetime.now().timestamp()

            # Insert new object into database.
            obj['id'] = max_id + 1
            yield from self.database[self.name].insert(obj)

        # Publish event that the object chaned.
        del obj['_id']
        self.app_session.publish(self.get_uri('changed'), [], object=obj)


class ViewSet:
    """
    Container for interactions for database objects.
    """
    name = None
    uri_prefix = None

    def __init__(self, app_session):
        """
        Initialize viewset. Binds app_session, database connection and
        logger to the instance.
        """
        self.app_session = app_session
        self.database = app_session.database
        self.logger = app_session.logger
        return super().__init__()

    def get_uri(self, action):
        """
        Returns the URI of WAMP procedures or PubSub events according to
        the given action.
        """
        if self.name is None:
            raise NotImplementedError('ViewSet name is missing.')
        if self.uri_prefix is None:
            raise NotImplementedError('ViewSet URI prefix is missing.')
        return '{}.{}{}'.format(
            self.uri_prefix,
            action,
            self.name)

    @coroutine
    def register_viewset(self):
        """
        Registeres all procedures that are mixed in.
        """
        yield from super().register_viewset()


class ObjectViewSet(ViewSet, ListObjectsMixin, CreateObjectsMixin):
    """
    Interactions for database objects: List, Create, Update, Destroy.
    """
    pass
