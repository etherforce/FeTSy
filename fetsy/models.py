from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy


class Status(models.Model):
    """
    Model for status a ticket can have.
    """
    name = models.CharField(
        ugettext_lazy('Name'),
        primary_key=True,
        max_length=255)

    def __str__(self):
        return self.pk


class Ticket(models.Model):
    """
    Model for tickets.
    """
    content = models.TextField(ugettext_lazy('Content'))
    status = models.ForeignKey(
        Status,
        verbose_name=ugettext_lazy('Status'))
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=ugettext_lazy('Assignee'),
        null=True,
        blank=True)

    def __str__(self):
        return self.pk
