from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.index, name='index'),
    path('pending-orders', views.pending_orders, name='pending_orders'),
    path('shipped-orders', views.shipped_orders, name='shipped_orders'),
    path('delivered-orders', views.delivered_orders, name='delivered_orders'),
]
