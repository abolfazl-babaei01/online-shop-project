from django import forms


class CouponApplyForm(forms.Form):
    code = forms.CharField(label='کد تخفیف', max_length=50)
