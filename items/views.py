from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from items.models import Item, Shop
from items.forms import ItemForm, ShopForm

@staff_member_required
def create_item(request):

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            
            form.save()
            
            return redirect('menu')
        
    else:
        form = ItemForm()
        
    context = {
        'form' : form
    }
    return render(request, 'items/create_item.htm', context)
        
@staff_member_required
def update_item(request, pk):
    
    item = get_object_or_404(Item, pk = pk)
    
    if request.method == "POST":
        form = ItemForm(request.POST, instance = item)
        if form.is_valid():
            
            form.save()
            
            return redirect('menu')
        
    else:
        form = ItemForm(instance = item)
        
    context = {
        'form' : form,
        'item' : item
    }
    return render(request, 'items/update_item.htm', context)

@staff_member_required
def register_shop(request):

    if request.method == "POST":
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            
            form.save()
            
            return redirect('menu')
        
    else:
        form = ShopForm()
        
    context = {
        'form' : form
    }
    return render(request, 'items/register_shop.htm', context)

# Create your views here.
