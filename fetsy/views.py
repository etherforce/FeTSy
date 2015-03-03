from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .models import Status, Tag, Ticket
from .serializers import TicketSerializer, UserSerializer


class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet to list, retrieve, create, update and destroy tickets.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to list and retrieve all users.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
