from django.db import models
from django.contrib.auth.models import User
from core.models import Product
# Create your models here.


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    stars = models.FloatField()
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment


class ShopReview(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    stars = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment
