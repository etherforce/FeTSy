from django.conf.urls import include, patterns, url
from django.contrib import admin
from rest_framework import routers

from .views import TicketViewSet

router = routers.DefaultRouter()
router.register(r'tickets', TicketViewSet)

urlpatterns = patterns(
    '',
    url(r'^rest/', include(router.urls)),
    # TODO: Remove the next lines when auth views are present.
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)
