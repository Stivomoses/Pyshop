from django.shortcuts import render, redirect
from .models import *
from likes.models import LikedProduct, LikedBrand
from reviews.models import *
from cart.models import Cart
from general.functions import calculate_cart_quantity, guest_user_id, recently_viewed
import json
from django.http import JsonResponse


def index(request):
    guest_user_id(request)

    if request.method == 'POST':
        data = json.loads(request.body)
        search_value = data['searchValue']

        starts_with_results = list(Product.objects.filter(
            name__startswith=search_value).values())

        for p in starts_with_results:
            if p['discounted_price']:
                p['discounted_price'] = f"{p['discounted_price']:,}"
                p['price'] = f"{p['price']:,}"
            else:
                p['price'] = f"{p['price']:,}"

        contains_results = list(Product.objects.filter(
            name__contains=search_value).values())

        for c_product in contains_results:  # O(n2)
            exists = False
            for s_product in starts_with_results:
                if s_product['id'] == c_product['id']:
                    exists = True
                    break
            if not exists:
                if c_product['discounted_price']:
                    c_product['discounted_price'] = f"{c_product['discounted_price']:,}"
                    c_product['price'] = f"{c_product['price']:,}"
                else:
                    c_product['price'] = f"{c_product['price']:,}"
                starts_with_results.append(c_product)

        return JsonResponse(starts_with_results, safe=False)
    else:
        products = Product.objects.all().order_by('-id')
        discounts_above_10 = []

        for product in products:
            if len(discounts_above_10) < 10:
                if product.discounted_price:
                    percentage_discount = round(
                        ((product.price - product.discounted_price)/product.price)*100)
                    if percentage_discount >= 10:
                        discounts_above_10.append(
                            {'product': product, 'percentage_discount': percentage_discount})
            else:
                break

        bargainable_products = Product.objects.filter(
            is_price_bargainable='Yes').order_by('-id')[0:10]

        reviews = ShopReview.objects.all().order_by('-stars')[0:10]
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)
            cart_quantity = calculate_cart_quantity(cart)
        else:
            cart = Cart.objects.filter(
                session_id=request.session['guestuserid'])
            cart_quantity = calculate_cart_quantity(cart)

        return render(request, 'home.html', {
            'categories': Category.objects.all(),
            'new_arrivals': products[0:10],
            'discounts_above_10': discounts_above_10,
            'bargainable_products': bargainable_products,
            'reviews': reviews,
            'cart_quantity': cart_quantity
        })


def new_arrivals(request):
    guest_user_id(request)
    if request.user.is_authenticated:
        likes = list(LikedProduct.objects.filter(user=request.user).values())
    else:
        likes = list(LikedProduct.objects.filter(
            session_id=request.session['guestuserid']).values())

    return render(request, 'products.html', {
        'products': Product.objects.all().order_by('-id')[0:10],
        'title': 'New Arrivals',
        'likes': likes,
    })


def top_discounts(request):
    guest_user_id(request)
    products = []
    for product in Product.objects.all().order_by('-id'):
        if product.discounted_price:
            percentage_discount = round(
                ((product.price - product.discounted_price)/product.price)*100)
            if percentage_discount >= 10:
                products.append(product)
    if request.user.is_authenticated:
        likes = list(LikedProduct.objects.filter(user=request.user).values())
    else:
        likes = list(LikedProduct.objects.filter(
            session_id=request.session['guestuserid']).values())

    return render(request, 'products.html', {
        'products': products,
        'title': 'Top Discounts',
        'likes': likes,
    })


def bargainable_prices(request):
    guest_user_id(request)

    if request.user.is_authenticated:
        likes = list(LikedProduct.objects.filter(user=request.user).values())
    else:
        likes = list(LikedProduct.objects.filter(
            session_id=request.session['guestuserid']).values())

    return render(request, 'products.html', {
        'products': Product.objects.filter(
            is_price_bargainable='Yes').order_by('-id'),
        'title': 'Bargainable Prices',
        'likes': likes,
    })


def product_details(request, product_id):
    guest_user_id(request)

    product = Product.objects.get(id=product_id)

    return render(request, 'details.html', {
        'product': product,
        'page': 'product_details'
    })


def brands(request):
    guest_user_id(request)

    if request.user.is_authenticated:
        likes = list(LikedBrand.objects.filter(user=request.user).values())
    else:
        likes = list(LikedBrand.objects.filter(
            session_id=request.session['guestuserid']).values())

    return render(request, 'brands.html', {
        'brands': FeaturedBrand.objects.all().order_by('-id'),
        'categories': Category.objects.all(),
        'likes': likes
    })


def brand_products(request, brand_id):
    guest_user_id(request)

    brand = FeaturedBrand.objects.get(id=brand_id)
    products = brand.products.all().order_by('-id')
    categories = []

    for product in products:
        if product.category.category_name and (product.category.category_name not in categories):
            categories.append(product.category.category_name)

    return render(request, 'brand-products.html', {
        'brand': brand,
        'categories': categories,
        'products': products
    })


def brand_products_details(request, brand_id, product_id):
    guest_user_id(request)
    recently_viewed(request, product_id)

    brand = FeaturedBrand.objects.get(id=brand_id)
    product = brand.products.get(id=product_id)
    images = product.images.all()
    sizes = product.sizes.all()
    category = product.category
    if category:
        related_products = category.products.exclude(
            id=product_id).exclude(brand_name=None).order_by('-id')
    else:
        related_products = brand.products.all().order_by('-id')
    reviews = ProductReview.objects.filter(
        product_id=product_id).order_by('-stars')

    if request.user.is_authenticated:
        is_liked = LikedProduct.objects.filter(
            product_id=product_id, user=request.user)
    else:
        is_liked = LikedProduct.objects.filter(
            product_id=product_id, session_id=request.session['guestuserid'])

    return render(request, 'details.html', {
        'brand': brand,
        'product': product,
        'images': images,
        'sizes': sizes,
        'related_products': related_products[:15],
        'reviews': reviews[:10],
        'is_liked': is_liked,
        'page': 'brand_details'
    })


def add_product(request):
    if request.method == 'POST':
        try:
            category_id = int(request.POST['category'])
            category = Category.objects.get(id=category_id)
        except ValueError:
            category = None

        try:
            brand_id = int(request.POST['brand'])
            brand = FeaturedBrand.objects.get(id=brand_id)
        except ValueError:
            brand = None
        name = request.POST['name']
        price = int(request.POST['price'])

        try:
            discounted_price = int(request.POST['discounted-price']) or None
        except ValueError:
            discounted_price = None
        bargainable = request.POST['bargainable']
        description = request.POST['description'] or None
        cover_image = request.FILES['cover-image']
        other_images = request.FILES.getlist('other-images')
        sizes = request.POST['sizes']

        product = Product.objects.create(
            category=category,
            brand_name=brand,
            cover_image=cover_image,
            name=name,
            price=price,
            discounted_price=discounted_price,
            is_price_bargainable=bargainable,
            description=description
        )
        
        other_images.insert(0,cover_image)
        for image in other_images:
            ProductImage.objects.create(product=product, image=image)

        if sizes:
            for size in sizes.split(','):
                SizeVariation.objects.create(
                    product=product,
                    size=size
                )

        return redirect('home:index')
    else:
        brands = FeaturedBrand.objects.all().order_by('brand_name')
        categories = Category.objects.all().order_by('category_name')

        return render(request, 'add-product.html', {
            'categories': categories,
            'brands': brands
        })
