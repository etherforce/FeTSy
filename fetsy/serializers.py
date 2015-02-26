from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Status, Ticket


class StatusSerializer(serializers.ModelSerializer):
    """
    Serializer for all possible status of a ticket.
    """
    class Meta:
        model = Status
        fields = ('name', )


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer for tickets.
    """
    assignee = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = (
            'id',
            'content',
            'status',
            'assignee', )

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
            'assignee', )


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
