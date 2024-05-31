from django.shortcuts import render, redirect

from order.models import Cart
# Create your views here.
from .models import Product
from order.views import getOrCreateCart
from order.models import CartItem

def index(request):
    cart = getOrCreateCart(request)

    products = Product.objects.all().values('id', 'name', 'price', 'stock')
    cart_items = CartItem.objects.filter(cart=cart).select_related('product')

    cart_products = [
        {
            'product_id': item.product.id,
            'name': item.product.name,
            'price': item.product.price,
            'quantity': item.quantity
        } for item in cart_items
    ]

    cart_product_ids = [item['product_id'] for item in cart_products]

    return render(request, 'store/index.html', {
        'products': products,
        'cart_products': cart_products,
        'cart_product_ids': cart_product_ids,
        'total_items': cart.totalItems(),
        'total_price': cart.totalPrice(),
    })

def gotoLogin(request):
    return redirect('accounts:login')

def gotoSignup(request):
    return redirect('accounts:sign-up')