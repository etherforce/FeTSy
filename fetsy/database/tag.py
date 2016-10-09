from asyncio import Lock, coroutine

from jsonschema import ValidationError, validate

new_tag_lock = Lock()

new_tag_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "New tag",
    "description": "A new tag for tickets",
    "type": "object",
    "properties": {
        "name": {
            "description": "The name of the tag",
            "type": "string"
        },
        "color": {
            "description": "The color of the tag.",
            "type": "string",
            "enum": [
                "default",
                "primary",
                "success",
                "info",
                "warning",
                "danger"
            ]
        },
        "weight": {
            "description": "The weight of the tag compared with other tags. "
                           "Tags should be sorted by ascending weight.",
            "type": "integer"
        }
    },
    "additionalProperties": False,
    "required": [
        "name",
        "color",
        "weight"
    ]
}

changed_ticket_schema = {}  #TODO


class ListTag:
    """
    Interactions to list some or all tags.
    """
    @coroutine
    def onJoin(self, details):
        yield from self.register(self.list_tags, 'org.fetsy.listTags')
        next_method = super().onJoin(details)
        if next_method is not None:
            yield from next_method

    @coroutine
    def list_tags(self, *args, **kwargs):
        """
        Async method to get some tags from the database.
        """
        # TODO: Use filtering here.
        self.logger.debug('Remote procedure list_tags called.')
        curser = self.database.tags.find()
        tags = []
        while (yield from curser.fetch_next):
            tag = curser.next_object()
            del tag['_id']
            tags.append(tag)
        return tags


class CreateTag:
    """
    Interactions to create a new tag.
    """
    @coroutine
    def onJoin(self, details):
        yield from self.register(self.new_tag, 'org.fetsy.newTag')
        next_method = super().onJoin(details)
        if next_method is not None:
            yield from next_method

    @coroutine
    def new_tag(self, *args, **kwargs):
        """
        Async method to create a new tag in the database.
        """
        self.logger.debug('Remote procedure new_tag called.')
        try:
            tag = self.validate_new_tag(kwargs.get('tag'))
        except ValidationError as e:
            result = {
                'type': 'error',
                'details': e.message}
        else:
            yield from self.save_new_tag(tag)
            success = 'Tag {} successfully created.'.format(tag['id'])
            result = {
                'type': 'success',
                'details': success}
        return result

    def validate_new_tag(self, tag):
        """
        Validates data for new tags.
        """
        if tag is None:
            raise ValidationError('Tag data is missing')
        validate(tag, new_tag_schema)
        return tag

    @coroutine
    def save_new_tag(self, tag):
        """
        Async method to store a new tag in the database. Adds a new 'id'
        property.
        """
        with (yield from new_tag_lock):
            # Fetch biggest ID from database.
            max_id_key = 'maxID'
            pipeline = [
                {'$sort': {'id': 1}},
                {'$group': {'_id': None, max_id_key: {'$last': '$id'}}}]
            future_result = yield from self.database.tags.aggregate(
                pipeline, cursor=False)
            if future_result['result']:
                max_id = future_result['result'][0][max_id_key]
            else:
                max_id = 0
            # TODO: For use of Mongo >= 2.5
            # curser = self.database.tickets.aggregate(pipeline)
            # while (yield from curser.fetch_next):
            #    result = curser.next_object()

            # Insert new tag in database.
            tag['id'] = max_id + 1
            yield from self.database.tags.insert(tag)

        # Publish changedTag event.
        del tag['_id']
        self.publish('org.fetsy.changedTag', [], tag=tag)


class Tag(ListTag, CreateTag):
    """
    Interactions for tags.
    """
    pass
