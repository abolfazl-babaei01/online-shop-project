from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ShopUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.


@admin.register(ShopUser)
class ShopUserAdmin(UserAdmin):
    ordering = ['phone']
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = ShopUser

    list_display = ['phone', 'first_name', 'last_name', 'is_staff', 'is_superuser']

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'secure_code')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', )})
                )

    add_fieldsets = (
        (None, {'fields': ('phone', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'secure_code')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', )})
                )
