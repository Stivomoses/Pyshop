from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from core.models import Product
from general.functions import guest_user_id

# Create your views here.


def index(request):
    guest_user_id(request)

    recent_products = []
    if "recently" in request.session:
        for id in request.session["recently"]:
            recent_products.append(Product.objects.get(id=id))

    return render(request, 'account.html', {
        'recent_products': recent_products
    })


def login_view(request):
    guest_user_id(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home:index')
        else:
            return render(request, 'login.html', {
                'form': LoginForm(request.POST),
                'message': 'Incorrect username or password'
            })
    else:
        return render(request, 'login.html', {
            'form': LoginForm()
        })


def logout_view(request):
    guest_user_id(request)
    logout(request)
    return render(request, 'login.html', {
        'form': LoginForm(),
        'message': 'Logged out'
    })


def signup(request):
    guest_user_id(request)
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

            # auto login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home:index')
        else:
            return render(request, 'signup.html', {
                'form': SignupForm(request.POST)
            })
    else:
        return render(request, 'signup.html', {
            'form': SignupForm()
        })


def notifications(request):
    return render(request, 'notifications.html')
