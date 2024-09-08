from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify-register/', views.verify_register_code, name='verify_register_code'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('otp-login/', views.otp_login, name='otp_login'),
    path('verify-otp-login/', views.verify_otp_login, name='verify_otp_login'),

    path('change-password/', views.change_password, name='change_password'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('profile/', views.profile, name='profile'),

    path('forget-password/', views.forget_password, name='forget_password'),
    path('reset-verify-phone/', views.reset_password, name='reset_verify_phone'),

]