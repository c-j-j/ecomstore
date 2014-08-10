from django.conf.urls import patterns, url
from ecomstore import settings

urlpatterns = patterns('accounts.views',
    (r'^register/$', 'register', {'SSL': settings.ENABLE_SSL,}, 'register'),
    url(r'^my_account/$', 'my_account', name='my_account'),
    url(r'^order_details/(?P<order_id>[-\w]+)/$', 'order_details', name='order_details'),
    url(r'^order_info/$', 'order_info', name='order_info'),
)

urlpatterns += patterns('django.contrib.auth.views',
    (r'^login/$', 'login', {
        'template_name': 'registration/login.html',
        'SSL': settings.ENABLE_SSL
    },'login'),)
