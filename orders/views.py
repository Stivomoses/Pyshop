from django.shortcuts import render
from general.functions import guest_user_id

# Create your views here.


def index(request):
    return render(request, 'orders.html', {})


def pending_orders(request):
    pass


def shipped_orders(request):
    pass


def delivered_orders(request):
    pass
