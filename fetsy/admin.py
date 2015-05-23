from django.contrib.admin import site
from django.utils.translation import ugettext_lazy

from .models import Tag, Ticket

site.site_title = site.site_header = ugettext_lazy('FeTSy site admin')
site.index_template = 'admin/custom-index.html'

site.register(Tag)
site.register(Ticket)
