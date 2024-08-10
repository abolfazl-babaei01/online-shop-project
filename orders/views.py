from django.shortcuts import render, redirect
from django.contrib.auth import login
from account.models import ShopUser
from .models import Order, OrderItem
from utils.KaveSms import send_sms_with_template, send_sms_normal
from django.contrib import messages
from .forms import PhoneVerificationForm, OrderForm
import random
from string import ascii_letters, digits
from cart.cart import Cart
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
import os
from django.conf import settings
from bidi.algorithm import get_display
import arabic_reshaper
from datetime import datetime, timedelta


# Create your views here.


def verify_phone(request):
    if request.user.is_authenticated:
        return redirect('orders:create_order')
    if request.method == 'POST':
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            tokens = {'token': ''.join(random.choices('0123456789', k=6))}
            print(tokens)
            request.session['verification_code'] = tokens['token']
            request.session['verification_phone'] = phone
            request.session['code_time'] = datetime.now().isoformat()
            # send_sms_with_template(receptor=phone, tokens=tokens, template='my_template_name_in_kave')
            messages.success(request, f'کد تائید با موفقیت به شماره ({phone}) ارسال شد')
            return redirect('orders:verify_code')
    else:
        form = PhoneVerificationForm()
    return render(request, 'forms/verify_phone.html', {'form': form})


def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            verification_phone = request.session['verification_phone']
            verification_code = request.session['verification_code']
            code_time = request.session['code_time']
            generation_code_time = datetime.fromisoformat(code_time)
            current_time = datetime.now()
            if current_time - generation_code_time > timedelta(seconds=10):
                messages.error(request, 'کد تایید معتبر نیست ')
            elif code == verification_code:
                user = ShopUser.objects.create_user(phone=verification_phone)
                random_password = ''.join(random.choices(ascii_letters + digits, k=8))
                print(random_password)
                user.set_password(random_password)
                user.save()
                # send_sms_normal(receptor=verification_phone, message=f'hi user/ your password is {random_password}')
                del request.session['verification_code']
                del request.session['verification_phone']
                login(request, user)
                return redirect('orders:create_order')
            else:
                messages.error(request, 'کد تایید اشتباه است')
    return render(request, 'forms/verify_code.html')


def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.buyer = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'],
                                         price=item['price'], weight=item['weight'])
            cart.clear()
            return redirect('product:product_list')
    else:
        form = OrderForm()
    return render(request, 'forms/create_order.html', {'form': form, 'cart': cart})


def order_list(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-created')
    return render(request, 'orders/order_list.html', {'orders': orders})


def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, buyer=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


def generate_pdf(request, order_id):
    order = Order.objects.get(id=order_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order_id}.pdf"'

    pdf = canvas.Canvas(response, pagesize=A4)

    font_path = os.path.join(settings.BASE_DIR, 'fonts', 'Arial/Arial Regular.ttf')
    pdfmetrics.registerFont(TTFont('Arial Regular', font_path))
    pdf.setFont('Arial Regular', 12)

    def draw_right_aligned_text(c, text, x, y):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        c.drawRightString(x, y, bidi_text)

    draw_right_aligned_text(pdf, f"شماره سفارش: {order.id}", 500, 750)
    draw_right_aligned_text(pdf, f"نام خریدار: {order.buyer.get_full_name()}", 500, 730)
    draw_right_aligned_text(pdf, f"تاریخ سفارش: {order.created.strftime('%Y/%m/%d')}", 500, 710)
    draw_right_aligned_text(pdf, f"نام: {order.first_name}", 500, 690)
    draw_right_aligned_text(pdf, f"نام خانوادگی: {order.last_name}", 500, 670)
    draw_right_aligned_text(pdf, f"شماره تلفن: {order.phone}", 500, 650)
    draw_right_aligned_text(pdf, f"کد پستی: {order.postal_code}", 500, 630)
    draw_right_aligned_text(pdf, f"استان: {order.province}", 500, 610)
    draw_right_aligned_text(pdf, f"شهر: {order.city}", 500, 590)
    draw_right_aligned_text(pdf, f"آدرس: {order.address}", 500, 570)

    pdf.showPage()
    pdf.save()

    return response
