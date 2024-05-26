from django.shortcuts import render, redirect

# Create your views here.
from .models import Product

def index(request):

    products = Product.objects.all().values('name', 'price')

    return render(request, 'store/index.html', {'products': products})

def goto_login(request):
    return redirect('accounts:login')

def goto_signup(request):
    return redirect('accounts:sign-up')