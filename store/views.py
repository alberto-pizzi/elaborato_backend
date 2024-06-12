from django.shortcuts import render, redirect,get_object_or_404

from order.models import Cart
# Create your views here.
from .models import Product, Category, Size, Color,ProductVariant
from order.views import get_or_create_cart
from order.models import CartItem
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Subquery


def header_data(request):
    cart = get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart).select_related('product')
    cart_products = [
        {
            'product_id': item.product.id,
            'name': item.product.title,
            'price': item.product.price,
            'quantity': item.product.quantity
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


def exclude_sizes(prod_id,prod_color_id):
    product_out_of_stock = ProductVariant.objects.filter(product_id=prod_id, color_id=prod_color_id, quantity=0).all()

    sizes_by_product = ProductVariant.objects.filter(product_id=prod_id).values_list('size_id', flat=True).distinct()

    sizes_by_color = (ProductVariant.objects.filter(product_id=prod_id, color_id=prod_color_id)
                      .values_list('size_id', flat=True).distinct())

    sizes_not_found = set(sizes_by_product) - set(sizes_by_color)
    sizes_not_found_list = [i for i in sizes_not_found]
    sizes_out_of_stock_list = [i.size_id for i in product_out_of_stock]

    sizes_to_exclude = list(set(sizes_out_of_stock_list + sizes_not_found_list))

    return sizes_to_exclude

def update_product_info(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('prod_id'))
        prod_color_id = int(request.POST.get('product_color_id'))

        new_prod = ProductVariant.objects.filter(product_id=prod_id, color_id=prod_color_id).first()
        new_price = new_prod.price

        new_image_url = new_prod.image_id.image.url


        data_response = {
            'sizes_out_of_stock': exclude_sizes(prod_id,prod_color_id),
            'new_price': new_price,
            'new_image_url': new_image_url
        }
        return JsonResponse({'status': 'success', 'message': 'JSON Success'} | data_response)
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'}, status=400)




def product_detail(request, gen, category, id):
    product = get_object_or_404(ProductVariant, id=id)
    base_product_id = product.product.id

    product_colors = (ProductVariant.objects.filter(product_id=base_product_id).values('color_id').distinct())
    colors = Color.objects.filter(id__in=product_colors).all()

    product_sizes = (ProductVariant.objects.filter(product_id=base_product_id).values('size_id').distinct())
    sizes = Size.objects.filter(id__in=product_sizes).all()



    #FIXME optimize redondancy
    data = {
        'product': product,
        'gender': gen,
        'category_slug': category,
        'category_name': category.capitalize(),
        'sizes': sizes,
        'colors': colors,
        'quantities': [i+1 for i in range(1, 19, 1)],
        'blocked_sizes': exclude_sizes(base_product_id,product.color),
    }

    return render(request, 'store/product-detail.html', data | header_data(request))

def store_view(request, gen):
    products = ProductVariant.objects.select_related('product').filter(Q(product__gender=gen) | Q(product__gender='Unisex'))

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


def search_view(request):

    if request.method == "GET":
        searched = request.GET.get('searched').strip()

        if searched:
            keywords = searched.split()
            query_objects = Q()
            for keyword in keywords:
                query_objects &= (
                    Q(title__icontains=keyword) |
                    Q(product__description__icontains=keyword) |
                    Q(color__color_name__icontains=keyword) |
                    Q(size__size_name__icontains=keyword)
                )
            products = ProductVariant.objects.select_related('product', 'color', 'size').filter(query_objects).distinct()
        else:
            return redirect('store:home')

        data = {
            'products': products,
            'searched': searched
        }

        return render(request, 'store/searched.html', data | header_data(request))

    return render(request, 'store/searched.html', header_data(request))
