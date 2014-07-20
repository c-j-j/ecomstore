import os
from django.conf.urls import patterns, include, url

from django.contrib import admin
from ecomstore import settings
from ecomstore.settings import BASE_DIR

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^catalog/$', 'preview.views.home', name='home'),
                       url(r'^admin/', include(admin.site.urls)),
)
