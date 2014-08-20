from django.conf.urls import patterns, url

urlpatterns = patterns('search.views',
            url(r'^results/$', 'results', {'template_name': 'search/results.html'}, 'search_results'),
                       )