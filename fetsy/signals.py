import json
import logging

from django.contrib.auth.models import User

from .models import Ticket
from .serializers import TicketSerializer

logger = logging.getLogger(__name__)


def model_change_logging(sender, instance, created=None, **kwargs):
    """
    Logs every change of Tags, Tickets and Users.
    """
    if sender == Ticket:
        serializer = TicketSerializer
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
