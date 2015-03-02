from django.contrib.admin import site

from .models import Tag, Ticket

site.register(Tag)
site.register(Ticket)
