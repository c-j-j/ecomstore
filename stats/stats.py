import base64
import os
from cart import cart
from catalog.models import Product
from ecomstore.settings import PRODUCTS_PER_ROW
from search import search
from search.models import SearchTerm
from stats.models import ProductView

TRACKING_ID = 'tracking_id'


def tracking_id(request):
    if request.session.get(TRACKING_ID, '') == '':
        request.session[TRACKING_ID] = cart.generate_random_id()
    return request.session[TRACKING_ID]


def recommended_from_search(request):
    common_words = frequent_search_words(request)

    matching = []
    for word in common_words:
        results = search.products(word).get('products', [])
        for result in results:
            if len(matching) < PRODUCTS_PER_ROW and not result in matching:
                matching.append(result)

    return matching


def frequent_search_words(request):
    searches = SearchTerm.objects.filter(tracking_id=tracking_id(request)) \
                   .values('q').order_by('-search_date')[0:10]

    search_string = ' '.join([search['q'] for search in searches])
    return sort_words_by_frequency(search_string)[0:3]


def sort_words_by_frequency(search_string):
    words = search_string.split()
    ranked_words = [[word, words.count(word)] for word in set(words)]
    sorted_words = sorted(ranked_words, key=lambda word: -word[1])
    return [p[0] for p in sorted_words]


def log_product_view(request, product):
    t_id = tracking_id(request)
    try:
        v = ProductView.objects.get(tracking_id=t_id, product=product)
        v.save()
    except ProductView.DoesNotExist:
        v = ProductView()
        v.product = product
        v.tracking_id = t_id
        v.ip_address = request.META.get('REMOTE_ADDR')
        v.user = None
        if request.user.is_authenticated():
            v.user = request.user
        v.save()


def recommended_from_views(request):
    t_id = tracking_id(request)
    viewed_products = get_recently_viewed_products(request)

    if viewed_products:
        # get all tracking ids who have viewed the list of products viewed by users
        product_views = ProductView.objects.filter(product__in=viewed_products).values('tracking_id')
        t_ids = [v['tracking_id'] for v in product_views]

        if t_ids:
            all_viewed_products = Product.active.filter(productview__tracking_id__in=t_ids)

            if all_viewed_products:
                other_viewed_products = ProductView.objects.filter(product__in=all_viewed_products)\
                    .exclude(product__in=viewed_products)

                if other_viewed_products:
                    return Product.active.filter(productview__in=other_viewed_products).distinct()


def get_recently_viewed_products(request):
    t_id = tracking_id(request)
    views = ProductView.objects.filter(tracking_id=t_id).values('product_id').order_by('-date')[0:PRODUCTS_PER_ROW]
    product_ids = [v['product_id'] for v in views]
    return Product.active.filter(id__in=product_ids)



