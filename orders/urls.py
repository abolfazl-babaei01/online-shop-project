from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('verify-phone/', views.verify_phone, name='verify_phone'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('create-order/', views.create_order, name='create_order'),
    path('order-list/', views.order_list, name='order_list'),
    path('order-detail/<int:order_id>', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/pdf/', views.generate_pdf, name='generate_pdf'),
]
