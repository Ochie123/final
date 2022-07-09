from django import forms
from django.forms.models import inlineformset_factory 
from .models import Product, Subcategory
SubcategoryFormSet = inlineformset_factory(Product, Subcategory, fields=['title','description'], extra=2,can_delete=True)