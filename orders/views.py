from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
import xlwt
from datetime import datetime, timedelta
from django.contrib import messages
 
from users.models import Customer
from items.models import Item
from orders.models import Order, OrderedItem
from items.constants import CATEGORIES
from orders.forms import OfferForm

from orders.utils import *

def index(request):
    return render(request, 'orders/index.htm')

def test_menu(request):
    
    vv_items = []
    sf_items = []
    tf_items = []
    of_items = []
    ff_items = []
    
    context = {
        'vv_items' : [],
        'sf_items' : [],
        'tf_items' : [],
        'of_items' : [],
        'ff_items' : [],
        'bt_shops' : [],
        'pg_shops' : [],
        'dd_shops' : [],
        'mr_shops' : [],
        'all_items' : [],
        'categories' : [],
    }
    
    for item in Item.objects.filter(stock__gte=1):
        category = (item.category).lower()
        context[category+"_items"].append(item)

    for item in Item.objects.filter(stock__gte=1):
        category = (item.shop.location).lower()
        shops = set(context.get(category+"_shops", []))
        shops.add(item.shop.name)
        context[category+"_shops"] = list(shops)
    
    context["all_items"] = [item for item in Item.objects.all()]
    context["categories"] = ["vv", "sf", "tf", "of", "ff"]

    #print(context)
   
    return render(request, 'orders/menu-admin.htm', context)

@login_required
def create_order(request):
    customer = get_object_or_404(Customer, user = request.user)
    order = Order.objects.create(
        customer = customer,
    )
    
    context = {
        'order' : order,
        'customer' : customer
    }
    
    return redirect('add_items', order.id)

@login_required
def add_items(request, pk):
    
    order = get_object_or_404(Order, pk = pk)
    ordered_items = list(OrderedItem.objects.filter(order = order))
    print(ordered_items)
    
    if request.method == "POST":
        
        data = dict(request.POST)

        items = Item.objects.all()

        for item in items:
            
            item_quantity = data[str(item.id)][0]

            if item_quantity is '':
                item_quantity = 0

            if int(item_quantity) >= 1:
                
                ordered_item = OrderedItem.objects.filter(
                    order = order,
                    item = item
                )
                
                if len(ordered_item)==0:
                    ordered_item = OrderedItem.objects.create(
                        order = order,
                        item = item
                    )
                    ordered_item.quantity += int(item_quantity)       
                    ordered_item.save()

                    ordered_items.append(ordered_item)
                else:
                    ordered_item = ordered_item[0]
                    ordered_item.quantity += int(item_quantity)       
                    ordered_item.save()
        
        # Calculate Price of Order
        order.save()
        
        return redirect('add_items', order.id)

    vv_items = []
    sf_items = []
    tf_items = []
    of_items = []
    ff_items = []
    
    context = {
        'vv_items' : [],
        'sf_items' : [],
        'tf_items' : [],
        'of_items' : [],
        'ff_items' : [],
        'bt_shops' : [],
        'pg_shops' : [],
        'dd_shops' : [],
        'mr_shops' : [],
        'all_items' : [],
        'categories' : [],
        'order' : order,
        'ordered_items' : ordered_items,
    }
    
    for item in Item.objects.filter(stock__gte=1):
        category = (item.category).lower()
        context[category+"_items"].append(item)

    for item in Item.objects.filter(stock__gte=1):
        category = (item.shop.location).lower()
        shops = set(context.get(category+"_shops", []))
        shops.add(item.shop.name)
        context[category+"_shops"] = list(shops)
    
    context["all_items"] = [item for item in Item.objects.all()]
    context["categories"] = ["vv", "sf", "tf", "of", "ff"]
    
    return render(request, 'orders/menu.htm', context)

@login_required
def finalize_order(request, pk):
    
    order = get_object_or_404(Order, pk = pk)
    ordered_items = OrderedItem.objects.filter(order = order)
    
    if len(ordered_items):
        now = datetime.now()
        order.date_placed = now.date()
        order.time_placed = now.time()
        order.date_placed = order.date_placed + timedelta(days=1) # due to the problems of timezone
        calculate_delivery_charge(order, ordered_items)
        calculate_grand_total_and_update_stocks(order, ordered_items)
        calculate_expected_delivery_time(order, ordered_items)
        order.finalized = True
        order.save()
        
        return redirect('order_summary', order.id)
        
    else:
        return redirect('add_items', order.id)
    
@login_required
def order_summary(request, pk):
    
    order = get_object_or_404(Order, pk = pk)
    ordered_items = OrderedItem.objects.filter(order = order)
    
    context = {
        'order' : order,
        'items' : ordered_items
    }
    
    return render(request, 'orders/order_summary.htm', context)

@login_required
def accept_order(request, pk):
    
    order = get_object_or_404(Order, pk = pk)
    order.delivered = True
    order.save()
    
    return redirect('feedback', order.pk)

@login_required
def delete_order(request, pk):
    try:
        Order.objects.filter(id=pk).delete()
        
        return redirect('index')
    except:
        return redirect('index')

@login_required
def feedback(request, pk):
    
    order = get_object_or_404(Order, pk = pk)
    ordered_items = OrderedItem.objects.filter(order = order)
    
    if request.method == "POST":
        
        data = dict(request.POST)
        print(data)
        for item in ordered_items:
            print(data.get(str(item.id))[0])
            item.rating = int(data.get(str(item.id))[0])
            item.save()
        
        calculate_item_ratings(ordered_items)
        
        return redirect('customer_dashboard')
        
    context = {
        'order' : order,
        'items' : ordered_items
    }
    
    return render(request, 'orders/feedback.htm', context)

@login_required
def past_transactions(request):
    
    customer = get_object_or_404(Customer, user = request.user)
    orders = Order.objects.filter(customer = customer, finalized = True)
    
    context = {
        'customer' : customer,
        'orders' : orders
    }
    
    return render(request, 'orders/past_transactions.htm', context)


# Admin Controls

@login_required
@staff_member_required
def generate_sales(request):
    
    today = date.today().strftime("%d%m%Y")
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = "attachment; filename=Sales_"+str(today)+".xlsx"

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Sales_"+str(today))

    #Writing the headers
    row = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = [
        'Category', 'Item ID', 'Item Name', 'Orders', 'Sales',
    ]

    for col in range(len(columns)):
        ws.write(row, col, columns[col], font_style)

    #Writing Orders data to the sheet
    font_style = xlwt.XFStyle()
    
    orders = Order.objects.filter(date_placed=date.today(), finalized = True)
    items = Item.objects.all()
    ordered_items = []
    
    for order in orders:
        ordered_items += OrderedItem.objects.filter(order = order)
    
    net_sales = 0
    for c in range(len(CATEGORIES)):
        category = str(CATEGORIES[c][0])
        for i in items:
            if i.category == category:
                
                count = 0
                sales = 0
                
                for o_item in ordered_items:
                    if o_item.item == i:
                        count += o_item.quantity
                        sales += o_item.price
                
                net_sales += sales
                        
                row += 1
                ws.write(row, 0, i.category, font_style)
                ws.write(row, 1, i.id, font_style)
                ws.write(row, 2, i.name, font_style)
                ws.write(row, 3, count, font_style)
                ws.write(row, 4, sales, font_style)
                
    row += 1
    ws.write(row, 3, "TOTAL SALES", font_style)
    ws.write(row, 4, net_sales, font_style)
    
    wb.save(response)
        
    return response
    
@login_required
@staff_member_required
def notify_offers(request):
    
    customers = Customer.objects.all()
    
    if request.method=="POST":
        
        form = OfferForm(request.POST)
        if form.is_valid():
            
            offer_text = form.cleaned_data['offer_text']

            mail_customers(customers, offer_text)
            
            
            return redirect('staff_dashboard')
            
    else:
        form = OfferForm()
    
    context = {
        'form' : form
    }  
      
    return render(request, 'orders/notify_offers.htm', context)
# Create your views here.
