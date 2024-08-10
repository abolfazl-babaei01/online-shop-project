from django import forms
from account.models import ShopUser
from orders.models import Order


class PhoneVerificationForm(forms.Form):
    phone = forms.CharField(max_length=11, label='شماره تلفن')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if ShopUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError('This phone already exists')
        if len(phone) != 11:
            raise forms.ValidationError('phone must be 11 digits')
        if not phone.isdigit():
            raise forms.ValidationError('phone must be digits')
        if not phone.startswith('09'):
            raise forms.ValidationError('phone must start with 09')
        return phone


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'address', 'postal_code', 'province', 'city']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 11:
            raise forms.ValidationError('phone must be 11 digits')
        if not phone.isdigit():
            raise forms.ValidationError('phone must be digits')
        if not phone.startswith('09'):
            raise forms.ValidationError('phone must start with 09')
        return phone
