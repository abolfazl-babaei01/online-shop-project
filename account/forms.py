from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import ShopUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ['phone', 'first_name', 'last_name', 'secure_code', 'is_staff', 'is_superuser', 'is_active']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone and ShopUser.objects.exclude(id=self.instance.id).filter(phone=phone):
            raise forms.ValidationError('This phone number already')

        if not phone.isdigit():
            raise forms.ValidationError('This phone number must contain only digits')

        if not phone.startswith('09'):
            raise forms.ValidationError('This phone number must start with 09 digits')

        if len(phone) != 11:
            raise forms.ValidationError('This phone number must contain at least 11 digits')
        return phone


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = ShopUser
        fields = ['phone', 'first_name', 'last_name', 'secure_code', 'is_staff', 'is_superuser', 'is_active']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone and ShopUser.objects.exclude(id=self.instance.id).filter(phone=phone):
            raise forms.ValidationError('This phone number already')

        if not phone.isdigit():
            raise forms.ValidationError('This phone number must contain only digits')

        if not phone.startswith('09'):
            raise forms.ValidationError('This phone number must start with 09 digits')

        if len(phone) != 11:
            raise forms.ValidationError('This phone number must contain  11 digits')
        return phone


class RegisterModelForm(forms.ModelForm):
    password = forms.CharField(max_length=15, widget=forms.PasswordInput, label='کلمه عبور')

    class Meta:
        model = ShopUser
        fields = ['first_name', 'last_name', 'phone']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone and ShopUser.objects.exclude(id=self.instance.id).filter(phone=phone):
            raise forms.ValidationError('This phone number already')

        if not phone.isdigit():
            raise forms.ValidationError('This phone number must contain only digits')

        if not phone.startswith('09'):
            raise forms.ValidationError('This phone number must start with 09 digits')

        if len(phone) != 11:
            raise forms.ValidationError('This phone number must contain  11 digits')
        return phone


class CodeVerificationForm(forms.Form):
    code = forms.CharField(max_length=6, label='کد تایید')


class LoginForm(forms.Form):
    phone = forms.CharField(max_length=11, label='شماره تلفن')
    password = forms.CharField(max_length=15, widget=forms.PasswordInput, label='کلمه عبور')


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=15, widget=forms.PasswordInput, label='کلمه عبور فعلی')
    password1 = forms.CharField(max_length=15, widget=forms.PasswordInput, label='کلمه عبور جدید')
    password2 = forms.CharField(max_length=15, widget=forms.PasswordInput, label='تکرار کلمه عبور جدید')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = ShopUser
        fields = ['phone', 'first_name', 'last_name']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone and ShopUser.objects.exclude(id=self.instance.id).filter(phone=phone):
            raise forms.ValidationError('This phone number already')

        if not phone.isdigit():
            raise forms.ValidationError('This phone number must contain only digits')

        if not phone.startswith('09'):
            raise forms.ValidationError('This phone number must start with 09 digits')

        if len(phone) != 11:
            raise forms.ValidationError('This phone number must contain  11 digits')
        return phone


class ForgetPasswordForm(forms.Form):
    phone = forms.CharField(max_length=11, label='شماره تلفن')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone.isdigit():
            raise forms.ValidationError('This phone number must contain only digits')

        if not phone.startswith('09'):
            raise forms.ValidationError('This phone number must start with 09 digits')

        if len(phone) != 11:
            raise forms.ValidationError('This phone number must contain  11 digits')
        return phone
