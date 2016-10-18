from .viewset import ObjectViewSet


class Tag(ObjectViewSet):
    """
    Interactions for tags.
    """
    name = 'Tag'
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


changed_tag_schema = {}  #TODO
