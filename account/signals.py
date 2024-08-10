from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import ShopUser


@receiver(pre_save, sender=ShopUser)
def create_profile(sender, instance, **kwargs):
    if not instance.first_name:
        instance.first_name = 'کاربر' + instance.phone[-4:]
