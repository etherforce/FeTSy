from django.contrib.admin import ModelAdmin, site
from django.utils.translation import ugettext_lazy

from .models import Tag, Ticket

site.site_title = site.site_header = ugettext_lazy('FeTSy site admin')
site.index_template = 'admin/custom-index.html'


class TicketAdmin(ModelAdmin):
    """
    Model admin class for tickets.
    """
    list_per_page = 1000


site.register(Ticket, TicketAdmin)
site.register(Tag)
