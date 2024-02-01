from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.index, name='index'),
    path('add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('increase-cart', views.increase_cart, name='increase-cart'),
    path('decrease-cart', views.decrease_cart, name='decrease-cart'),
    path('delete-cart', views.delete_cart, name='delete'),
    path('empty-cart', views.empty_cart, name='empty-cart')
]
