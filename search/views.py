from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from search import search


def results(request, template_name="search/results.html"):
    q = request.GET.get('q', '')
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    matching = search.products(q).get('products')

    paginator = Paginator(matching, 10)

    try:
        results = paginator.page(page).object_list
    except (InvalidPage, EmptyPage):
        results = paginator.page(1).object_list

    search.store(request, q)
    page_title = 'Search Results for ' + q
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))



