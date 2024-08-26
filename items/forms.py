from django import forms
from items.models import Item, Shop

class ItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = ['name', 'description', 'shop', 'category', 'rate', 'stock', 'is_non_veg', 'image']
        

class ShopForm(forms.ModelForm):
    
    class Meta:
        model = Shop
        fields = ['name', 'location', 'area']
        