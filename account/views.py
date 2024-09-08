import string

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterModelForm, LoginForm, ChangePasswordForm, UpdateProfileForm, ForgetPasswordForm, \
    CodeVerificationForm, OtpLoginForm
from .models import ShopUser
from utils.KaveSms import send_sms_normal, send_sms_with_template
import random
from string import ascii_letters, digits
from datetime import datetime, timedelta
import time
import json



# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            request.session['user_data'] = form.cleaned_data
            tokens = {'token': ''.join(random.choices('0123456789', k=6))}
            request.session['verification_code'] = tokens['token']
            request.session['code_time'] = datetime.now().isoformat()
            print(tokens)

            # sen sms to user phone number
            # phone = form.cleaned_data['phone']
            # send_sms_with_template(receptor=phone, tokens=tokens, template='my_template_name')
            return redirect('account:verify_register_code')
    else:
        form = RegisterModelForm()
    return render(request, 'forms/register.html', {'form': form})


def verify_register_code(request):
    if request.method == 'POST':
        form = CodeVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            code_time = request.session.get('code_time')
            verification_code = request.session.get('verification_code')
            code_generation_time = datetime.fromisoformat(code_time)
            current_time = datetime.now()

            if current_time - code_generation_time > timedelta(seconds=60):
                form.add_error('code', 'کد تایید اعتبار ندارد')
            elif code == verification_code:
                user_data = request.session.get('user_data')
                user = ShopUser(first_name=user_data['first_name'], last_name=user_data['last_name'],
                                phone=user_data['phone'])
                user.set_password(user_data['password'])
                user.save()

                del request.session['user_data']
                del request.session['verification_code']
                del request.session['code_time']

                login(request, user)
                return redirect('product:index')
            else:
                form.add_error('code', 'کد تایید اشتباه است')

    else:
        form = CodeVerificationForm()
    return render(request, 'forms/verify_register_code.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, phone=form.cleaned_data['phone'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                form.add_error('phone', 'This phone number or password is incorrect.')
    else:
        form = LoginForm()
    return render(request, 'forms/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('product:index')


def otp_login(request):
    if request.method == 'POST':
        form = OtpLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            user = ShopUser.objects.filter(phone=phone).first()
            if user is not None:
                tokens = {'token': ''.join(random.choices('0123456789', k=6))}
                request.session['verification_token'] = tokens['token']
                request.session['user_phone'] = phone
                request.session['token_time'] = datetime.now().isoformat()
                # send_sms_with_template(receptor=phone, tokens=tokens, template='your template')
                print(tokens['token'])
                return redirect('account:verify_otp_login')
            else:
                form.add_error('phone', 'شماره تلفن وارد شده نا معتبر می باشد')


    else:
        form = OtpLoginForm()
    return render(request, 'forms/otp_login.html', {'form': form})


def verify_otp_login(request):
    if request.method == 'POST':
        form = CodeVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            token_time = request.session['token_time']
            current_time = datetime.now()
            token_generation_time = datetime.fromisoformat(token_time)
            if current_time - token_generation_time > timedelta(seconds=60):
                form.add_error('code', 'کد تایید اعتبار ندارد')
            elif code == request.session['verification_token']:
                phone = request.session['user_phone']
                user = ShopUser.objects.filter(phone=phone).first()
                login(request, user)
                del request.session['verification_token']
                del request.session['user_phone']
                del request.session['token_time']
                return redirect('product:index')
            else:
                form.add_error('code', 'کد تایید اشتیاه می باشد')
    else:
        form = CodeVerificationForm()
    return render(request, 'forms/verify_otp_login.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(ShopUser, id=request.user.id)
            correct_password = user.check_password(form.cleaned_data['old_password'])
            if correct_password:
                user.set_password(form.cleaned_data['password1'])
                user.save()
                login(request, user)
                return redirect('product:index')
            else:
                form.add_error('old_password', 'old password is incorrect.')

    else:
        form = ChangePasswordForm()
    return render(request, 'forms/change_password.html', {'form': form})


def profile(request):
    user = get_object_or_404(ShopUser, id=request.user.id)

    return render(request, 'account/profile.html', {"user": user})


def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'forms/update_profile.html', {'form': form})


def forget_password(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']

            try:
                user = ShopUser.objects.get(phone=phone)
                if user:
                    tokens = {'token': ''.join(random.choices('0123456789', k=6))}
                    # send token sms for user
                    # send_sms_with_template(phone, tokens, 'my template name in site kavengaar')
                    request.session['forget_token'] = tokens['token']
                    request.session['forget_phone'] = phone
                    request.session['forget_code_time'] = datetime.now().isoformat()
                    print(tokens)
                    return redirect('account:reset_verify_phone')

            except ShopUser.DoesNotExist:
                form.add_error('phone', 'phone is invalid.')
    else:
        form = ForgetPasswordForm()
    return render(request, 'forms/forget_password.html', {'form': form})


def reset_password(request):
    if request.method == 'POST':
        token = None
        phone = None
        forget_code_time = None
        code = request.POST.get('code')
        if code:
            try:
                phone = request.session.get('forget_phone')
                token = request.session['forget_token']
                forget_code_time = request.session.get('forget_code_time')
            except (KeyError, ValueError):
                messages.error(request, 'Code Not Found')
            generation_code_time = datetime.fromisoformat(forget_code_time)
            current_time = datetime.now()

            if current_time - generation_code_time > timedelta(seconds=10):
                messages.error(request, 'کد تائید اعتبار ندارد')
            elif code == token:
                user = ShopUser.objects.get(phone=phone)
                random_password = ''.join(random.choices(ascii_letters + digits, k=8))
                print(random_password)
                user.set_password(random_password)
                user.save()
                # --Send Message To User--
                # message = f 'hi your account password changed successfully\n Your new password is : {random_password}'
                # send_sms_normal(phone, message)
                del request.session['forget_token']
                del request.session['forget_phone']
                del request.session['forget_code_time']
                messages.success(request, 'hi your account password changed successfully')
                return redirect('account:login')
            else:
                messages.error(request, 'verify code is invalid')
                return redirect('account:reset_verify_phone')
    return render(request, 'forms/reset_verify_phone.html')
