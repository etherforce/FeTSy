from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .models import Status, Ticket
from .serializers import (
    StatusSerializer,
    TicketCreateUpdateSerializer,
    TicketSerializer,
    UserSerializer
)


class StatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to list and retrieve all possible status of a ticket.
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet to list, retrieve, create, update and destroy tickets.
    """
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            serializer = TicketCreateUpdateSerializer
        else:
            serializer = TicketSerializer
        return serializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to list and retrieve all users.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
