from django.contrib.auth import get_user_model
from rest_framework import metadata, viewsets

from .models import Tag, Ticket
from .serializers import TicketSerializer


class TicketViewSetMetadata(metadata.SimpleMetadata):
    """
    Custom metadata class to add users and tags to OPTIONS.
    """
    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)
        ticket_choices = {}
        ticket_choices['tags'] = [
            {'value': tag.pk,
             'display_name': tag.name,
             'color_css_class': tag.color_css_class}
            for tag in Tag.objects.all()]
        ticket_choices['status'] = [
            {'value': value,
             'display_name': display_name}
            for value, display_name in Ticket.STATUS_CHOICES]
        ticket_choices['priority'] = [
            {'value': value,
             'display_name': display_name}
            for value, display_name in Ticket.PRIORITY_CHOICES]
        ticket_choices['assignee'] = [
            {'value': user.pk,
             'display_name': user.get_full_name() or user.username}
            for user in get_user_model().objects.all()]
        metadata['ticket_choices'] = ticket_choices
        return metadata


class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet to list, retrieve, create, update and destroy tickets.
    """
    metadata_class = TicketViewSetMetadata
    queryset = Ticket.objects.all().select_related('assignee')
    serializer_class = TicketSerializer
