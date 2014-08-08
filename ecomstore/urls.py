import os
from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('',
                       # Examples:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('catalog.urls')),
                       url(r'^cart/', include('cart.urls')),
                       url(r'^checkout/', include('checkout.urls')),
)

handler404 = 'ecomstore.views.file_not_found_404'

