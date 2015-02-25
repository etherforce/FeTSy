from rest_framework import viewsets

from .models import Ticket
from .serializers import TicketCreateUpdateSerializer, TicketSerializer


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
