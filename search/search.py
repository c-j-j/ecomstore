from django.db.models import Q
from catalog.models import Product
from search.models import SearchTerm

STRIP_WORDS = ['a','an','the']

def store(request, q):

    #only store for queries longer than two characters
    if len(q) > 2:
        term = SearchTerm()
        term.q = q
        term.ip_address = request.META.get('REMOTE_ADDR')
        term.user = None

        if request.user.is_authenticated():
            term.user = request.user
        term.save()


#search for products
def products(search_text):
    words = prepare_words(search_text)
    products = Product.active.all()
    results = {}
    results['products'] = []

    for word in words:
        results['products']=products.filter(Q(name__icontains=word) | Q(description__icontains=word))

    return results


def prepare_words(search_text):
    words = search_text.split()

    for ignored_word in STRIP_WORDS:
        if ignored_word in words:
            words.remove(ignored_word)

    return words[0:5]   #for performance reasons, only allow 5 words to be searched