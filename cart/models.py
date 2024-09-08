from django.db import models

# Create your models here.


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)  # ذخیره به صورت درصد (مثلاً 0.15 برای 15٪)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.code
