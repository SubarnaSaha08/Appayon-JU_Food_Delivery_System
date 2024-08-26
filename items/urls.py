from django.urls import path
from items.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('create_item', create_item, name='create_item'),
    
    path('<int:pk>/update_item', update_item, name='update_item'),
    
    path('register_shop', register_shop, name='register_shop'),
    
]
