from django.db import models
from core.models import FeaturedBrand, Product
from django.contrib.auth.models import User

# Create your models here.


class LikedProduct(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.product.name


class LikedBrand(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(
        FeaturedBrand, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.brand.brand_name
