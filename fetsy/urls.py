from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from rest_framework import routers

from .views import StatusViewSet, TagViewSet, TicketViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'status', StatusViewSet)
router.register(r'tags', TagViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'users', UserViewSet)

urlpatterns = patterns(
    '',
    url(r'^rest/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$',
        'django.contrib.auth.views.logout_then_login',
        name='logout'),
    url(r'^$',
        login_required(ensure_csrf_cookie(
            TemplateView.as_view(template_name='home.html'))),
        name='home'),
)
