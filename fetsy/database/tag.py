from asyncio import coroutine

from pymongo import ASCENDING

from .viewset import ObjectViewSet


class Tag(ObjectViewSet):
    """
    Interactions for tags.
    """
    name = 'Tag'
    list_sort = [('weight', ASCENDING)]
    uri_prefix = 'org.fetsy'
    new_object_schema = {
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
                "description": "The weight of the tag compared with other "
                               "tags. Tags should be sorted by ascending "
                               "weight.",
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

    @coroutine
    def register_viewset(self):
        """
        Registeres all default procedures for this viewset. Additionally
        adds index on weight field.
        """
        yield from super().register_viewset()
        yield from self.database[self.name].create_index('weight')
        self.logger.debug("Index for Tag's weight field created.")
