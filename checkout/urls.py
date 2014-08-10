from django.conf.urls import patterns, url

urlpatterns = patterns('checkout.views',
                       url(r'^$', 'show_checkout', {'template_name': 'checkout/checkout.html'}, 'show_checkout'),
                       url(r'^receipt/$', 'checkout_receipt', {'template_name': 'checkout/receipt.html'}, 'checkout_receipt'),
)
