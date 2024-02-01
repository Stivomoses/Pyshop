from django.db import models
from django.contrib.auth.models import User
from core.models import Product

# Create your models here.


class CustomerOrder(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    phone_number = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.CharField(max_length=15)
