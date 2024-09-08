from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from cart.cart import Cart
from product.models import Product
from django.utils import timezone
from .models import Coupon
from .forms import CouponApplyForm


# Create your views here.

@require_POST
def add_to_cart(request, product_id):
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, pk=product_id)
        cart.add(product)
        context = {
            'items_count': len(cart),
            'total_price': cart.get_total_price()
        }
        return JsonResponse(context)
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'Invalid Request'})


# def cart_detail(request):
#     cart = Cart(request)
#     form = CouponApplyForm()
#     coupon = None
#     discount = 0
#     total_price_after_discount = None
#
#     if 'apply_coupon' in request.POST:
#         form = CouponApplyForm(request.POST)
#         if form.is_valid():
#             code = form.cleaned_data['code']
#             try:
#                 coupon = Coupon.objects.filter(code=code, active=True, valid_from__lte=timezone.now(),
#                                                valid_to__gte=timezone.now()).first()
#                 request.session['coupon_id'] = coupon.id
#             except Exception as e:
#                 print(f'line 45 {e}')
#                 request.session['coupon_id'] = None
#
#     if 'coupon_id' in request.session.keys():
#         try:
#             coupon = Coupon.objects.get(id=request.session['coupon_id'])
#             discount = coupon.discount
#         except Exception as e:
#             print(f'line 53 {e}')
#
#     try:
#         cart_final_price = cart.get_final_price()
#         discount_amount = cart_final_price * coupon.discount
#         total_price_after_discount = cart_final_price - discount_amount
#     except Exception as e:
#         print(f'line 60 {e}')
#     context = {
#         'cart': cart,
#         'form': form,
#         'coupon': coupon,
#         'discount': discount,
#         'total_price_after_discount': total_price_after_discount,
#     }
#     return render(request, 'cart/detail.html', context)


def cart_detail(request):
    cart = Cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'cart/detail.html', context)

@require_POST
def update_quantity(request):
    item_id = request.POST.get('item_id')
    action = request.POST.get('action')
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, pk=item_id)
        if action == 'increase':
            cart.add(product)
        elif action == 'decrease':
            cart.decrease(product)

        context = {
            'items_count': len(cart),
            'total_price': cart.get_total_price(),
            'total': cart.cart[item_id]['quantity'] * cart.cart[item_id]['price'],
            'quantity': cart.cart[item_id]['quantity'],
            'post_price': cart.get_post_price(),
            'final_price': cart.get_final_price(),
            'success': True
        }
        return JsonResponse(context)
    except Exception as e:
        print(f'update_quantity error: {e}')


@require_POST
def remove_item(request):
    item_id = request.POST.get('item_id')
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, pk=item_id)
        cart.remove(product)
        context = {

            'items_count': len(cart),
            'total_price': cart.get_total_price(),
            'post_price': cart.get_post_price(),
            'final_price': cart.get_final_price(),
            'success': True,
            'empty_cart': True if len(cart) == 0 else False

        }
        return JsonResponse(context)
    except Exception as e:
        print(f'remove item error: {e}')
        return JsonResponse({'status': 'error'})
