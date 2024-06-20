from django.shortcuts import render, redirect,get_object_or_404

from order.models import Cart
# Create your views here.
from .models import Product, Category, Size, Color,ProductVariant
from order.views import get_or_create_cart
from order.models import CartItem
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Subquery
from django.contrib import messages


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
    products = ProductVariant.objects.select_related('product').filter(quantity__gt=0).all().order_by('-product__date_added')[:total_latest_shown]

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

        if new_prod.image_id:
            new_image_url = new_prod.image_id.image.url
        else:
            new_image_url = None


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



def filters(request,products):
    applied_filters = {}
    if request.method == 'GET':
        applied_filters['min_price'] = request.GET.get('min_price')
        applied_filters['max_price'] = request.GET.get('max_price')
        applied_filters['colors'] = request.GET.getlist('color_filtered')
        applied_filters['sizes'] = request.GET.getlist('size_filtered')

        if 'reset' not in request.GET:
            if applied_filters['min_price'] and int(applied_filters['min_price']) >= 0:
                products = products.filter(price__gte=applied_filters['min_price'])

            if applied_filters['max_price'] and int(applied_filters['max_price']) >= 0:
                products = products.filter(price__lte=applied_filters['max_price'])

            if applied_filters['colors']:
                selected_colors = Color.objects.filter(id__in=applied_filters['colors'])
                if selected_colors.exists():
                    applied_filters['colors'] = list(selected_colors.values_list('id', flat=True))
                    products = products.filter(color__in=applied_filters['colors']).distinct()

            if applied_filters['sizes']:
                selected_sizes = Size.objects.filter(id__in=applied_filters['sizes'])
                if selected_sizes.exists():
                    applied_filters['sizes'] = list(selected_sizes.values_list('id', flat=True))
                    products = products.filter(size__in=applied_filters['sizes']).distinct()

        return products, applied_filters

    return None, applied_filters



def store_view(request, gen):
    products = ProductVariant.objects.select_related('product').filter(Q(quantity__gt=0) & (Q(product__gender=gen) | Q(product__gender='Unisex')))

    colors = Color.objects.all().distinct()
    sizes = Size.objects.all().distinct()

    products,applied_filters = filters(request, products)

    data = {
        'products': products,
        'gender': gen,
        'applied_filters': applied_filters,
        'colors': colors,
        'sizes': sizes
    }

    return render(request, 'store/store.html', data | header_data(request))


def category_view(request, gen, category):

    products = ProductVariant.objects.select_related('product__category', 'product').filter(Q(quantity__gt=0) & Q(product__category__category_slug=category) & (Q(product__gender=gen) | Q(product__gender='Unisex')) )

    colors = Color.objects.all().distinct()
    sizes = Size.objects.all().distinct()

    products, applied_filters = filters(request, products)

    data = {
        'products': products,
        'gender': gen,
        'category_slug': category,
        'category_name': category.capitalize(),
        'applied_filters': applied_filters,
        'colors': colors,
        'sizes': sizes
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
                    Q(size__size_name__icontains=keyword) |
                    Q(product__category__name__icontains=keyword) |
                    Q(product__gender__icontains=keyword)
                )
            products = ProductVariant.objects.select_related('product', 'color', 'size').filter(query_objects, quantity__gt=0).distinct()
        else:
            return redirect('store:home')

        data = {
            'products': products,
            'searched': searched
        }

        return render(request, 'store/searched.html', data | header_data(request))

    return render(request, 'store/searched.html', header_data(request))
