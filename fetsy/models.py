from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy


class Ticket(models.Model):
    """
    Model for tickets.
    """
    STATUS_CHOICES = (
        (1, ugettext_lazy('New')),
        (2, ugettext_lazy('Work in progress')),
        (3, ugettext_lazy('Closed')), )

    PRIORITY_CHOICES = (
        (1, ugettext_lazy('Very low')),
        (2, ugettext_lazy('Low')),
        (3, ugettext_lazy('Medium')),
        (4, ugettext_lazy('High')),
        (5, ugettext_lazy('Very high')), )

    content = models.TextField(
        ugettext_lazy('Content'))
    tags = models.TextField(
        ugettext_lazy('Tags'),
        help_text=ugettext_lazy('Separate tags with newline.'),
        blank=True)
    status = models.PositiveIntegerField(
        ugettext_lazy('Status'),
        choices=STATUS_CHOICES,
        default=1)
    priority = models.PositiveIntegerField(
        ugettext_lazy('Priority'),
        choices=PRIORITY_CHOICES,
        default=3)
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=ugettext_lazy('Assignee'),
        null=True,
        blank=True)
    created = models.DateTimeField(
        ugettext_lazy('Created'),
        auto_now_add=True)
    period = models.PositiveIntegerField(
        ugettext_lazy('Period (in minutes)'),
        default=120)

    class Meta:
        verbose_name = ugettext_lazy('Ticket')
        verbose_name_plural = ugettext_lazy('Tickets')

    def __str__(self):
        return str(self.pk)
