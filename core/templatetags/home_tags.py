from django import template
from likes.models import LikedProduct, LikedBrand

register = template.Library()


@register.filter(name='calculate_percentage_discount')
def calculate_percentage_discount(discounted_price, original_price):
    return round(((original_price - discounted_price)/original_price)*100)


@register.filter(name='prices_filter')
def prices_filter(price):
    return f"{price:,}"


@register.filter(name='prices_filter')
def prices_filter(price):
    return f"{price:,}"


@register.filter(name='likes_filter')
def likes_filter(product_id):
    isLiked = LikedProduct.objects.filter(product_id=product_id)
    if isLiked:
        return 'fill'
    else:
        return 'outline'


@register.filter(name='brands_likes_filter')
def brands_likes_filter(brand_id):
    isLiked = LikedBrand.objects.filter(brand_id=brand_id)
    if isLiked:
        return 'fill'
    else:
        return 'outline'
