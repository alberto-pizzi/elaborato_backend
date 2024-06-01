from django.shortcuts import render, redirect,get_object_or_404

from order.models import Cart
# Create your views here.
from .models import Product, ProductVariant
from order.views import get_or_create_cart
from order.models import CartItem

def index(request):
    cart = get_or_create_cart(request)

    total_latest_shown = 6
    products = ProductVariant.objects.select_related('product').all().order_by('-product__date_added')[:total_latest_shown]
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

    return render(request, 'store/index.html', {
        'products': products,
        'cart_products': cart_products,
        'cart_product_ids': cart_product_ids,
        'total_items': cart.total_items(),
        'total_price': cart.total_price(),
        'genders': set([gender[0] for gender in Product.GENDERS])
    })

def goto_login(request):
    return redirect('accounts:login')

def goto_signup(request):
    return redirect('accounts:sign-up')

def goto_cart(request):
    return redirect('order:cart-overview')

def product_detail(request, id):
    product = get_object_or_404(ProductVariant, id=id)
    return render(request, 'store/product-detail.html', {'product': product})