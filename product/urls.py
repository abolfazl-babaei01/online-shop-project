from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('products/<str:category_slug>', views.product_list, name='product_list_by_category'),
    path('products/detail/<int:pk>/<slug:slug>', views.product_detail, name='product_detail'),
    path('like-product/<int:product_id>/', views.like_product, name='like_product'),
    path('add-comment/', views.add_comment, name='add_comment'),
    path('search/', views.search, name='search')
]