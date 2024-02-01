from django.contrib import admin
from .models import Cart

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    readonly_fields = ('user', 'product', 'quantity', 'created_at')


admin.site.register(Cart, CartAdmin)
