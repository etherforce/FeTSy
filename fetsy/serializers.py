from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Status, Tag, Ticket


class StatusSerializer(serializers.ModelSerializer):
    """
    Serializer for all possible status of a ticket.
    """
    class Meta:
        model = Status
        fields = ('name', )


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for all possible tags of a ticket.
    """
    class Meta:
        model = Tag
        fields = ('name', 'color_css_class', )


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer for tickets.
    """
    tags = TagSerializer(many=True)
    assignee = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = (
            'id',
            'content',
            'status',
            'tags',
            'assignee',
            'created', )

    def get_assignee(self, value):
        if value.assignee is not None:
            name = value.assignee.get_full_name() or value.assignee.username
        else:
            name = None
        return name


class TicketCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating tickets.
    """
    class Meta:
        model = Ticket
        fields = (
            'id',
            'content',
            'status',
            'assignee',
            'created', )


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for users.
    """
    name = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'name', )

    def get_name(self, value):
        return value.get_full_name() or value.username
