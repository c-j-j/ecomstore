from django import forms
from search.models import SearchTerm


class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchTerm

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        #'Search' will appear by default. when the form is clicked, the default text is cleared
        default_text = 'Search'
        self.fields['q'].widget.attrs['value'] = default_text
        self.fields['q'].widget.attrs['onfocus'] = "if (this.value=='" + default_text + "')this.value = ''"

    include = ('q',)