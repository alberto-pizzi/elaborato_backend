from django.shortcuts import render, redirect,get_object_or_404

from order.models import Cart
# Create your views here.
from .models import Product, ProductVariant, Category, Size
from order.views import get_or_create_cart
from order.models import CartItem
from django.db.models import Q


def header_data(request):
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
    categories = Category.objects.all()

    data = {
        'cart_products': cart_products,
        'cart_product_ids': cart_product_ids,
        'total_items': cart.total_items(),
        'total_price': cart.total_price(),
        'genders': [gender[0] for gender in Product.GENDERS],
        'categories': categories
    }
    return data


def index(request):
    total_latest_shown = 6
    products = ProductVariant.objects.select_related('product').all().order_by('-product__date_added')[:total_latest_shown]

    data = {
        'products': products,
    }

    return render(request, 'store/index.html', data | header_data(request))

def goto_login(request):
    return redirect('accounts:login')

def goto_signup(request):
    return redirect('accounts:sign-up')

def goto_cart(request):
    return redirect('order:cart-overview')

def product_detail(request, gen, category, id):
    product = get_object_or_404(ProductVariant, id=id)
    base_product_id = product.product.id
    sizes = (ProductVariant.objects.filter(product_id=base_product_id).select_related('product', 'size')
             .values('size__size_name').distinct())

    colors = (ProductVariant.objects.filter(product_id=base_product_id).select_related('product', 'color')
             .values('color__color_name').distinct())

    #FIXME optimize redondancy
    data = {
        'product': product,
        'gender': gen,
        'category_slug': category,
        'category_name': category.capitalize(),
        'sizes': sizes,
        'colors': colors
    }

    return render(request, 'store/product-detail.html', data | header_data(request))

def store_view(request, gen):
    products = ProductVariant.objects.select_related('product').filter(product__gender=gen)

    data = {
        'products': products,
        'gender': gen,
    }

    return render(request, 'store/store.html', data | header_data(request))


def category_view(request, gen, category):
    if gen == 'Kid' or gen == 'kid':
        products = ProductVariant.objects.select_related('product__category', 'product').filter(
            Q(product__category__category_slug=category) & Q(product__gender=gen))
    else:
        products = ProductVariant.objects.select_related('product__category', 'product').filter(Q(product__category__category_slug=category) & (Q(product__gender=gen) | Q(product__gender='Unisex')) )

    data = {
        'products': products,
        'gender': gen,
        'category_slug': category,
        'category_name': category.capitalize()

    }

    return render(request, 'store/store.html', data | header_data(request))