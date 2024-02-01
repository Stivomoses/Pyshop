from django.db import models
from django.contrib.auth.models import User
from core.models import Product, SizeVariation, ProductImage

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='carts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_variation = models.ForeignKey(
        ProductImage, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    size = models.ForeignKey(
        SizeVariation, models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.session_id
