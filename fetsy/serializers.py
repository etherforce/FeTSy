from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Ticket


class TagListField(serializers.ListField):
    """
    Field serializing tags. It transforms string (with newlines) to list
    and reverse.
    """
    def to_representation(self, data):
        return [item for item in data.splitlines()]

    def to_internal_value(self, data):
        return '\n'.join(super().to_internal_value(data))


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for users.
    """
    name = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'name', )

    def get_name(self, value):
        return value.get_full_name() or value.username


class UserRelatedField(serializers.RelatedField):
    """
    Field for serializing users as assignees in tickets.
    """
    def to_representation(self, value):
        """
        Returns serialized data using UserSerializer.
        """
        return UserSerializer(value).data

    def to_internal_value(self, data):
        """
        Validates data and returns the respective User object. Data should be
        a dictionary with an 'id' element.
        """
        if type(data) != dict or data.get('id') is None:
            raise serializers.ValidationError(
                "Invalid data. You must provide a dictionary with an 'id' "
                "element.")
        try:
            user = self.get_queryset().get(pk=data['id'])
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError(
                'Invalid data. User with id %d does not exist.' % data['id'])
        return user

    # TODO: Think whether to change server output so that OPTIONS contains
    #       valid JSON in choices field or keep the fix in client's
    #       JavaScript.
    #       See: rest_framework.relations.RelatedField.choices
    #
    # @property
    # def choices(self):
    #    return OrderedDict([
    #        (
    #            json.dumps(self.to_representation(item)),
    #            str(item)
    #        )
    #        for item in self.queryset.all()
    #    ])


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer for tickets.
    """
    assignee = UserRelatedField(
        queryset=get_user_model().objects.all(),
        required=False)
    tags = TagListField()

    class Meta:
        model = Ticket
        fields = (
            'id',
            'content',
            'tags',
            'status',
            'priority',
            'assignee',
            'created',
            'period', )
