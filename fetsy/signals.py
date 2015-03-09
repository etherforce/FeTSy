import json
import logging

from django.contrib.auth.models import User

from .models import Tag, Ticket
from .serializers import TagSerializer, TicketSerializer, UserSerializer

logger = logging.getLogger(__name__)


def model_change_logging(sender, instance, created=None, **kwargs):
    """
    Logs every change of Tags, Tickets and Users.
    """
    if sender == Tag:
        serializer = TagSerializer
    elif sender == Ticket:
        serializer = TicketSerializer
    elif sender == User:
        serializer = UserSerializer
    else:
        serializer = None

    if serializer:
        if created:
            action = 'created'
        elif created is not None:
            action = 'updated'
        else:
            action = 'deleted'
        log = {
            'model': sender.__name__,
            'action': action,
            'data': serializer(instance).data}
        logger.info(json.dumps(log))
