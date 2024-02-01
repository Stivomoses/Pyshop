from django.shortcuts import render
from .models import ProductReview, ShopReview
from django.http import JsonResponse
import json
# Create your views here.


def index(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        star = data['star']
        comment = data['comment']
        user_exists = ShopReview.objects.filter(user=request.user)
        if not user_exists:
            ShopReview.objects.create(
                user=request.user, stars=star, comment=comment)

            return JsonResponse('Added', safe=False)
        else:
            return JsonResponse('Already Added', safe=False)
    else:
        reviews = ShopReview.objects.all().order_by('-id')
        totalReviews = reviews.count()

        try:
            is_reviewed = ShopReview.objects.filter(user=request.user)
        except:
            is_reviewed = False

        one_stars = 0
        two_stars = 0
        three_stars = 0
        four_stars = 0
        five_stars = 0

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

        try:
            averageRating = round((total_ratings/totalReviews), 1)
        except ZeroDivisionError:
            averageRating = 5.0

        return render(request, 'general-reviews.html', {
            'reviews': reviews,
            'totalreviews': totalReviews,
            'averagerating': averageRating,
            'fivestars': five_stars,
            'fourstars': four_stars,
            'threestars': three_stars,
            'twostars': two_stars,
            'onestars': one_stars,
            'isreviewed': is_reviewed

        })


def product_reviews(request, product_id):
    reviews = ProductReview.objects.filter(product=product_id).order_by('-id')
    totalReviews = reviews.count()

    one_stars, two_stars, three_stars, four_stars, five_stars = 0, 0, 0, 0, 0

    for review in reviews:
        if review.stars == 1.0:
            one_stars += 1
        elif review.stars == 2.0:
            two_stars += 1
        elif review.stars == 3.0:
            three_stars += 1
        elif review.stars == 4.0:
            four_stars += 1
        else:
            five_stars += 1

    total_ratings = (five_stars*5) + (four_stars*4) + \
        (three_stars*3) + (two_stars*2) + (one_stars*1)

    try:
        average_rating = round((total_ratings/totalReviews), 1)
    except ZeroDivisionError:
        average_rating = 5.0

    return render(request, 'product-reviews.html', {
        'reviews': reviews,
        'productid': product_id,
        'totalreviews': totalReviews,
        'average_rating': average_rating,
        'fivestars': five_stars,
        'fourstars': four_stars,
        'threestars': three_stars,
        'twostars': two_stars,
        'onestars': one_stars

    })
