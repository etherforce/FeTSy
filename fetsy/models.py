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


class Tag(models.Model):
    """
    Model for tags. A ticket can have multiple tags.
    """
    COLORS = (
        ('default', ugettext_lazy('Grey')),
        ('primary', ugettext_lazy('Dark blue')),
        ('success', ugettext_lazy('Green')),
        ('info', ugettext_lazy('Light blue')),
        ('warning', ugettext_lazy('Yellow')),
        ('danger', ugettext_lazy('Red')), )

    name = models.CharField(
        ugettext_lazy('Name'),
        primary_key=True,
        max_length=255)
    color_css_class = models.CharField(
        ugettext_lazy('Color'),
        choices=COLORS,
        default='default',
        max_length=255)
    weight = models.IntegerField(
        ugettext_lazy('Weight (for ordering'),
        help_text=ugettext_lazy(
            'Tags with a higher weight appear behind other tags.'),
        default=0)

    class Meta:
        ordering = ('weight', )
        verbose_name = ugettext_lazy('Tag')
        verbose_name_plural = ugettext_lazy('Tags')

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
    tags = models.ManyToManyField(
        Tag,
        verbose_name=ugettext_lazy('Tags'),
        null=True,
        blank=True)
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=ugettext_lazy('Assignee'),
        null=True,
        blank=True)
    created = models.DateTimeField(
        ugettext_lazy('Created'),
        auto_now_add=True)

    def __str__(self):
        return str(self.pk)
