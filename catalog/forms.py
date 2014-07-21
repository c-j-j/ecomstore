from django import forms
from catalog.models import Product

__author__ = 'Chris'

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product

    def clean_price(self):
        if self.cleaned_data['price'] <=0:
            raise forms.ValidationError('Price must be greater than zero.')
        return self.cleaned_data['price']
