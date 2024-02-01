from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
from general.functions import guest_user_id

# Create your views here.


def index(request):
    guest_user_id(request)

    if request.user.is_authenticated:
        likes = LikedProduct.objects.filter(user=request.user)
    else:
        likes = LikedProduct.objects.filter(
            session_id=request.session['guestuserid'])

    return render(request, 'likes.html', {
        'likes': likes,
        'likes_count': likes.count(),
        'page': 'likes'
    })


def liked_brands(request):
    guest_user_id(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        brand_id = data['brandId']
        action = data['action']
        if action == 'like':
            if request.user.is_authenticated:
                is_liked = LikedBrand.objects.filter(
                    user=request.user, brand_id=brand_id)
                if not is_liked:
                    LikedBrand.objects.create(
                        user=request.user, brand_id=brand_id, session_id=request.session['guestuserid'])
                    return JsonResponse({'status': 'liked'})
                else:
                    return JsonResponse({'status': 'already liked'})
            else:
                is_liked = LikedBrand.objects.filter(
                    session_id=request.session['guestuserid'], brand_id=brand_id)
                if not is_liked:
                    LikedBrand.objects.create(
                        session_id=request.session['guestuserid'], brand_id=brand_id)
                    return JsonResponse({'status': 'liked'})
                else:
                    return JsonResponse({'status': 'already liked'})
        else:
            if request.user.is_authenticated:
                brand = LikedBrand.objects.filter(
                    user=request.user, brand_id=brand_id)
                if brand:
                    brand.delete()
                    return JsonResponse({'status': 'unliked'})
                else:
                    return JsonResponse({'status': 'already unliked'})
            else:
                brand = LikedBrand.objects.filter(
                    session_id=request.session['guestuserid'], brand_id=brand_id)
                if brand:
                    brand.delete()
                    return JsonResponse({'status': 'unliked'})
                else:
                    return JsonResponse({'status': 'already unliked'})

    else:
        if request.user.is_authenticated:
            brands = LikedBrand.objects.filter(user=request.user)
        else:
            brands = LikedBrand.objects.filter(
                session_id=request.session['guestuserid'])
        return render(request, 'likes.html', {
            'brands': brands,
            'brands_count': brands.count(),
            'page': 'brands'
        })


def update_like(request):
    guest_user_id(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['productId']
        action = data['action']
        if action == 'like':
            if request.user.is_authenticated:
                is_liked = LikedProduct.objects.filter(
                    user=request.user, product_id=product_id)
                if not is_liked:
                    LikedProduct.objects.create(
                        user=request.user, product_id=product_id, session_id=request.session['guestuserid'])
                    return JsonResponse({'status': 'liked'})
                else:
                    return JsonResponse({'status': 'already liked'})
            else:
                is_liked = LikedProduct.objects.filter(
                    session_id=request.session['guestuserid'], product_id=product_id)
                if not is_liked:
                    LikedProduct.objects.create(
                        session_id=request.session['guestuserid'], product_id=product_id)
                    return JsonResponse({'status': 'liked'})
                else:
                    return JsonResponse({'status': 'already liked'})
        else:
            if request.user.is_authenticated:
                like = LikedProduct.objects.filter(
                    user=request.user, product_id=product_id)
                if like:
                    like.delete()
                    return JsonResponse({'status': 'unliked'})
                else:
                    return JsonResponse({'status': 'already unliked'})
            else:
                like = LikedProduct.objects.filter(
                    session_id=request.session['guestuserid'], product_id=product_id)
                if like:
                    like.delete()
                    return JsonResponse({'status': 'unliked'})
                else:
                    return JsonResponse({'status': 'already unliked'})
