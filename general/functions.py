# calculate cart total quantity
import random


def calculate_cart_quantity(cart):
    cart_quantity = 0
    for item in cart:
        cart_quantity += item.quantity
    return cart_quantity


# calculate cart total price
def calculate_cart_price(cart):
    cart_price = 0
    for item in cart:
        if item.product.discounted_price:
            cart_price += item.quantity * item.product.discounted_price
        else:
            cart_price += item.quantity * item.product.price
    return cart_price


# generate unique id for every session
def guest_user_id(request):
    if 'guestuserid' not in request.session:
        id = f"{random.randint(10000,1000000)}fhjhhsh{random.randint(10000,1000000)}serihrnb"
        request.session['guestuserid'] = id


# add products to recently viewed

def recently_viewed(request, product_id):
    if 'recently' not in request.session:
        request.session["recently"] = [product_id]
    else:
        if product_id in request.session["recently"]:
            request.session["recently"].remove(product_id)
            request.session["recently"].insert(0, product_id)
        else:
            request.session["recently"].insert(0, product_id)
            if len(request.session["recently"]) > 14:
                request.session["recently"].pop()

    request.session.modified = True
