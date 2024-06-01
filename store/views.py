from django.shortcuts import render, redirect,get_object_or_404

from order.models import Cart
# Create your views here.
from .models import Product, ProductVariant
from order.views import get_or_create_cart
from order.models import CartItem


def cart_data(request):
    cart = get_or_create_cart(request)
    # FIXME review if product or product_variant
    cart_items = CartItem.objects.filter(cart=cart).select_related('product')
    cart_products = [
        {
            'product_id': item.id,
            'name': item.name,
            'price': item.price,
            'quantity': item.quantity
        } for item in cart_items
    ]

    cart_product_ids = [item['product_id'] for item in cart_products]

    data = {
        'cart_products': cart_products,
        'cart_product_ids': cart_product_ids,
        'total_items': cart.total_items(),
        'total_price': cart.total_price(),
    }
    return data


def index(request):
    total_latest_shown = 6
    products = ProductVariant.objects.select_related('product').all().order_by('-product__date_added')[:total_latest_shown]

    products_data = {
        'products': products,
        'genders': [gender[0] for gender in Product.GENDERS]
    }

    return render(request, 'store/index.html', products_data | cart_data(request))

def goto_login(request):
    return redirect('accounts:login')

def goto_signup(request):
    return redirect('accounts:sign-up')

def goto_cart(request):
    return redirect('order:cart-overview')

def product_detail(request, id):
    product = get_object_or_404(ProductVariant, id=id)
    return render(request, 'store/product-detail.html', {'product': product} | cart_data(request))