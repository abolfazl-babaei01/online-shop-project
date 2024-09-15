from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('detail/', views.cart_detail, name='cart_detail'),
    path('update-quantity/', views.update_quantity, name='update_quantity'),
    path('remove-item/', views.remove_item, name='remove_item'),

]