from orders.models import Order, OrderedItem
from items.models import Item
from django.contrib.auth.models import User
import smtplib
from django.conf import settings
from django.core.mail import send_mail
import numpy as np
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import numpy as np

area_graph = np.array([
    [0, 4, np.inf, 4, np.inf, np.inf, np.inf, np.inf, np.inf, 4, 5],
    [4, 0, 1, np.inf, np.inf, 1, np.inf, np.inf, np.inf, np.inf, 1],
    [np.inf, 1, 0, 1, 1, 1, np.inf, np.inf, np.inf, np.inf, np.inf],
    [4, np.inf, 1, 0, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf],
    [np.inf, np.inf, 1, np.inf, 0, np.inf, 1, np.inf, np.inf, np.inf, np.inf],
    [np.inf, 1, 1, np.inf, np.inf, 0, np.inf, np.inf, np.inf, np.inf, np.inf],
    [np.inf, np.inf, np.inf, np.inf, 1, np.inf, 0, 1, 1, np.inf, np.inf],
    [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 1, 0, np.inf, np.inf, np.inf],
    [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 1, np.inf, 0, 1, np.inf],
    [4, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 1, 0, np.inf],
    [5, 1, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 0],
])

def floyd_warshall(graph):
    V = len(graph)

    dist = graph.copy()
    path = np.full((V, V), -1, dtype=int)

    for i in range(V):
        path[i][i] = i

    for k in range(V):
        for i in range(V):
            for j in range(V):
                new_dist = dist[i][k] + dist[k][j]
                if new_dist < dist[i][j]:
                    dist[i][j] = new_dist
                    path[i][j] = path[k][j]

    return dist

def calculate_grand_total_and_update_stocks(order, ordered_items):
    grand_total = 0
    for o_item in ordered_items:
        o_item.item.stock -= o_item.quantity
        grand_total += o_item.calculate_price()
        grand_total =  grand_total + int(order.delivery_charge)
        o_item.item.save()
        o_item.save()
        
    order.grand_total = grand_total
    order.save()
    
def calculate_expected_delivery_time(order, ordered_items):
    dist = floyd_warshall(area_graph)

    active_orders = Order.objects.filter(finalized=True, delivered = False)
    expected_del_time = (len(active_orders) * 5)
    customer_area = int(order.customer.area)
    max_distance = -1
    for o_item in ordered_items:
        shop_area = int(o_item.item.shop.area)
        if max_distance <= dist[shop_area-1][customer_area-1]:
            max_distance = dist[shop_area-1][customer_area-1]
            
    order.expected_time = expected_del_time + (max_distance * 5)
    order.save()
    
def calculate_delivery_charge(order, ordered_items):
    dist = floyd_warshall(area_graph)
    default_delivery_charge = 10
    customer_area = int(order.customer.area)
    max_distance = -1
    for o_item in ordered_items:
        shop_area = int(o_item.item.shop.area)
        if max_distance <= dist[shop_area-1][customer_area-1]:
            max_distance = dist[shop_area-1][customer_area-1]
    order.delivery_charge = default_delivery_charge + (max_distance * 5)
    order.save()
    
def calculate_item_ratings(ordered_items):
    
    for o_item in ordered_items:
        count_item = OrderedItem.objects.filter(item = o_item.item).count()
        curr_rating_total = (o_item.item.rating * count_item) + o_item.rating
        
        curr_rating = (curr_rating_total)/(count_item + o_item.quantity)
        o_item.item.rating = curr_rating
        o_item.item.save()
        o_item.save()
        
def mail_customers(customers, offer_text):
    for customer in customers:
        send_mail(
            'New Offer from Appayon!',
            offer_text,
            'jucse29.subarna.349@gmail.com',
            [customer.user.email],
            fail_silently=False,
        )
                