from django import template
from core.models import Product

register = template.Library()


@register.filter(name='average_filter')
def average_filter(average_rating):
    first_value, second_value = str(average_rating).split('.')
    if int(second_value) < 5:
        return f"{first_value}.0"
    elif int(second_value) >= 5:
        return f"{first_value}.5"


@register.filter(name='average_reviews')
def average_review(product_id):
    product = Product.objects.get(id=product_id)
    reviews = product.reviews.all()

    if reviews:
        total_reviews = reviews.count()

        one_stars, two_stars, three_stars, four_stars, five_stars = 0, 0, 0, 0, 0

        for review in reviews:
            if review.stars == 1:
                one_stars += 1
            elif review.stars == 2:
                two_stars += 1
            elif review.stars == 3:
                three_stars += 1
            elif review.stars == 4:
                four_stars += 1
            else:
                five_stars += 1

        total_ratings = (five_stars*5) + (four_stars*4) + \
            (three_stars*3) + (two_stars*2) + (one_stars*1)

        average_rating = round((total_ratings/total_reviews), 1)

        first_value, second_value = str(average_rating).split('.')
        if int(second_value) < 5:
            return f"{first_value}.0"
        elif int(second_value) >= 5:
            return f"{first_value}.5"
    else:
        return "5.0"


@register.filter(name='reviews_count')
def reviews_count(product_id):
    product = Product.objects.get(id=product_id)
    reviews = product.reviews.all()
    return reviews.count()
