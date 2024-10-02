from django.db import models
from product.models import Product
from account.models import ShopUser


# Create your models here.

class Order(models.Model):
    buyer = models.ForeignKey(ShopUser, related_name='orders', on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    phone = models.CharField(max_length=11, verbose_name='شماره تلفن')
    address = models.TextField(max_length=1200, verbose_name='آدرس کامل')
    postal_code = models.CharField(max_length=10, verbose_name='کد پستی')
    province = models.CharField(max_length=50, verbose_name='استان')
    city = models.CharField(max_length=50, verbose_name='شهر')
    final_cost_with_discount = models.PositiveIntegerField(null=True, blank=True, verbose_name='هزینه نهایی با تخفیف')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f'order {str(self.id)}'

    def get_total_cost(self):
        total = sum(item.get_cost() for item in self.items.all())
        return total

    def get_post_cost(self):
        weight = sum(item.get_weight() for item in self.items.all())
        if weight == 0:
            return 0
        elif weight < 1000:
            return 7000
        elif 1000 <= weight <= 1500:
            return 30000
        elif weight >= 2000:
            return 50000
        else:
            return 60000

    def get_final_cost(self):
        return self.get_total_cost() + self.get_post_cost()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    weight = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.quantity * self.price

    def get_weight(self):
        return self.quantity * self.weight
