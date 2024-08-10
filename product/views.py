from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from cart.cart import Cart
from product.models import Product, Category, Comment
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    context = {
        'products': products,
        'user': request.user,
        'categories': categories
    }
    return render(request, 'product/index.html', context)


def product_list(request, category_slug=None):
    products = Product.objects.all()
    categories = Category.objects.all()
    if category_slug:
        products = products.filter(category__slug=category_slug).all()

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    in_stock = request.GET.get('in_stock')
    special = request.GET.get('special')

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if in_stock == 'true':
        products = products.filter(inventory__gt=0)
    if special == 'true':
        products = products.filter(off__gt=0)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'product/product_list_ajax.html', {'products': products})

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'product/list.html', context)


def product_detail(request, pk, slug):
    product = get_object_or_404(Product, id=pk, slug=slug)
    context = {
        'product': product
    }
    return render(request, 'product/detail.html', context)


@login_required
@require_POST
def like_product(request, product_id):
    user = request.user
    try:
        product = get_object_or_404(Product, id=product_id)
        if user in product.likes.all():
            product.likes.remove(user)
            liked = False
        else:
            product.likes.add(user)
            liked = True
        data = {'liked': liked}
        return JsonResponse(data)
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'like product view error'})


@login_required
@require_POST
def add_comment(request):
    product_id = request.POST.get('product_id')
    title = request.POST.get('title')
    text = request.POST.get('text')
    if product_id:
        try:
            comment = Comment.objects.create(product_id=product_id, user_id=request.user.id, title=title, text=text)
            response_data = {
                'success': True,
                'comment': {
                    'title': comment.title,
                    'text': comment.text,
                    'first_name': request.user.first_name,
                    'created': comment.created.strftime("%d-%m-%Y")
                }
            }
            return JsonResponse(response_data)
        except Product.DoesNotExist as e:
            print(e)
            return JsonResponse({''})


def search(request):
    query = None
    results = []
    if 'q' in request.GET:
        query = request.GET.get('q')
        product_title = Product.objects.filter(name__icontains=query)
        product_description = Product.objects.filter(description__icontains=query)
        results = product_title | product_description
    return render(request, 'forms/search_products.html', {'results': results, 'query': query})