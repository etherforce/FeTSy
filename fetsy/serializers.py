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


class UserRelatedField(serializers.RelatedField):
    """
    Field for serializing users as assignees in tickets.
    """
    def to_representation(self, value):
        """
        Returns serialized data using UserSerializer.
        """
        return value.get_full_name() or value.username

    def to_internal_value(self, data):
        """
        Validates data and returns the respective User object. Data should be
        an integer.
        """
        if not isinstance(data, int):
            raise serializers.ValidationError(
                "Invalid data. You must provide an integer.")
        try:
            user = self.get_queryset().get(pk=data)
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError(
                'Invalid data. User with id %d does not exist.' % data)
        return user


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
