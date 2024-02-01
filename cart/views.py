from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import Cart
from general.functions import calculate_cart_price, calculate_cart_quantity, guest_user_id

# Create your views here.


def index(request):
    guest_user_id(request)

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user).order_by('id')
        cart_quantity = calculate_cart_quantity(cart_items)
        cart_price = calculate_cart_price(cart_items)
    else:
        cart_items = Cart.objects.filter(
            session_id=request.session['guestuserid']).order_by('id')
        cart_quantity = calculate_cart_quantity(cart_items)
        cart_price = calculate_cart_price(cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'cart_quantity': cart_quantity,
        'cart_price': cart_price,
    })


def add_to_cart(request):
    guest_user_id(request)

    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['productId']

        try:
            image_id = data['imageId']
        except KeyError:
            image_id = None

        try:
            size_id = data['sizeId']
        except KeyError:
            size_id = None

        if request.user.is_authenticated:
            exists = Cart.objects.filter(
                user=request.user, product_id=product_id)
            if exists:
                item = exists[0]
                item.quantity += 1
                item.save()
                item_quantity = item.quantity
            else:
                Cart.objects.create(
                    user=request.user, product_id=product_id, session_id=request.session['guestuserid'], image_variation_id=image_id, size_id=size_id)
                item_quantity = 1
        else:
            exists = Cart.objects.filter(
                session_id=request.session['guestuserid'], product_id=product_id)

            if exists:
                item = exists[0]
                item.quantity += 1
                item.save()
                item_quantity = item.quantity
            else:
                Cart.objects.create(
                    session_id=request.session['guestuserid'], product_id=product_id)
                item_quantity = 1
        return JsonResponse({'item_quantity': item_quantity})
    else:
        return redirect('cart:index')


def increase_cart(request):
    guest_user_id(request)

    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['productId']

        try:  # if condition can be used as well
            cart_item = Cart.objects.get(
                user=request.user, product_id=product_id)
            cart_item.quantity += 1
            cart_item.save()
            item_quantity = cart_item.quantity
            total_cart_quantity = calculate_cart_quantity(
                Cart.objects.filter(user=request.user))
            total_cart_price = calculate_cart_price(
                Cart.objects.filter(user=request.user))
        except:
            cart_item = Cart.objects.get(
                session_id=request.session['guestuserid'], product_id=product_id)
            cart_item.quantity += 1
            cart_item.save()
            item_quantity = cart_item.quantity
            total_cart_quantity = calculate_cart_quantity(
                Cart.objects.filter(session_id=request.session['guestuserid']))
            total_cart_price = calculate_cart_price(
                Cart.objects.filter(session_id=request.session['guestuserid']))

        return JsonResponse({'itemQuantity': item_quantity, 'totalCartQuantity': total_cart_quantity, 'totalCartPrice': f"{total_cart_price:,}"})
    else:
        return redirect('cart:index')


def decrease_cart(request):
    guest_user_id(request)

    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['productId']
        try:
            cart_item = Cart.objects.get(
                user=request.user, product_id=product_id)
            cart_item.quantity -= 1
            if cart_item.quantity == 0:
                cart_item.delete()
                item_quantity = 0
            else:
                cart_item.save()
                item_quantity = cart_item.quantity
            total_cart_quantity = calculate_cart_quantity(
                Cart.objects.filter(user=request.user))
            total_cart_price = calculate_cart_price(
                Cart.objects.filter(user=request.user))
        except:
            cart_item = Cart.objects.get(
                session_id=request.session['guestuserid'], product_id=product_id)
            cart_item.quantity -= 1
            if cart_item.quantity == 0:
                cart_item.delete()
                item_quantity = 0
            else:
                cart_item.save()
                item_quantity = cart_item.quantity
            total_cart_quantity = calculate_cart_quantity(
                Cart.objects.filter(session_id=request.session['guestuserid']))
            total_cart_price = calculate_cart_price(
                Cart.objects.filter(session_id=request.session['guestuserid']))

        return JsonResponse({'itemQuantity': item_quantity, 'totalCartQuantity': total_cart_quantity, 'totalCartPrice': f"{total_cart_price:,}"})
    else:
        return redirect('cart:index')


def delete_cart(request):
    guest_user_id(request)

    if request.method == 'POST':
        data = json.loads(request.body)
        cart_id = data['cartId']
        cart_item = Cart.objects.get(id=cart_id)
        cart_item.delete()

        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)
            total_cart_quantity = calculate_cart_quantity(cart)
            total_cart_price = calculate_cart_price(cart)
        else:
            cart = Cart.objects.filter(
                session_id=request.session['guestuserid'])
            total_cart_quantity = calculate_cart_quantity(cart)
            total_cart_price = calculate_cart_price(cart)

        return JsonResponse({'totalCartQuantity': total_cart_quantity, 'totalCartPrice': f"{total_cart_price:,}"})
    else:
        return redirect('cart:index')


def empty_cart(request):
    guest_user_id(request)

    if request.method == 'POST':
        try:
            cart = Cart.objects.filter(user=request.user)
        except:
            cart = Cart.objects.filter(
                session_id=request.session['guestuserid'])
        cart.delete()
        return JsonResponse({'status': 'deleted'})
    else:
        return redirect('cart:index')
