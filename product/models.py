from django.db import models
from django.shortcuts import reverse
from account.models import ShopUser


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(max_length=1200)
    price = models.PositiveIntegerField(default=0)
    off = models.PositiveIntegerField(default=0)
    new_price = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)
    inventory = models.PositiveIntegerField(default=1)
    likes = models.ManyToManyField(to=ShopUser, related_name='likes', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:product_detail', args=[self.id, self.slug])


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    file = models.ImageField(upload_to='products/%Y/%m')
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=400, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

        indexes = [
            models.Index(fields=['-created'])
        ]


class ProductFuture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='futures')
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name} - {self.value}'


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='محصول')
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر')
    title = models.CharField(max_length=255, verbose_name='عنوان دیدگاه')
    text = models.TextField(verbose_name='متن دیدگاه')
    is_accepted = models.BooleanField(default=True, verbose_name='پذیرفته شده')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
