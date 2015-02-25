from rest_framework import serializers

from .models import Ticket


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
            if value.assignee.first_name or value.assignee.last_name:
                name = ' '.join(
                    (value.assignee.first_name, value.assignee.last_name))
            else:
                name = value.assignee.username
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
