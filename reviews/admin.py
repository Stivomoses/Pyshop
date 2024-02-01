from django.contrib import admin
from .models import *

# Register your models here.


class ProductReviewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'stars', 'comment', 'created_at')


class ShopReviewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'stars', 'comment', 'created_at')
    readonly_fields = ('user', 'stars', 'comment', 'created_at')


admin.site.register(ProductReview, ProductReviewsAdmin)
admin.site.register(ShopReview, ShopReviewsAdmin)
