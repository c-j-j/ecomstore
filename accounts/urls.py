from django.conf.urls import patterns, url
from ecomstore import settings

urlpatterns = patterns('accounts.views',
    url(r'^register/$', 'register', name='register'),
    url(r'^my_account/$', 'my_account', {'template_name': 'registration/my_account.html'},name='my_account'),
    url(r'^order_details/(?P<order_id>[-\w]+)/$', 'order_details', name='order_details'),
    url(r'^order_info/$', 'order_info', name='order_info'),
)

urlpatterns += patterns('django.contrib.auth.views',
                        url(r'^login/$', 'login', {
                            'template_name': 'registration/login.html',
                        }, name='login'))
