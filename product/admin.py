from django.contrib import admin
from .models import *


# Register your models here.

class ImageInline(admin.StackedInline):
    model = Image
    extra = 0
    raw_id_fields = ['product']


class FutureInline(admin.TabularInline):
    model = ProductFuture
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'new_price', 'inventory']
    list_editable = ['price', 'inventory']
    prepopulated_fields = {'slug': ['name']}
    raw_id_fields = ['category']
    inlines = [ImageInline, FutureInline, CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'is_accepted']
    list_editable = ['is_accepted']



