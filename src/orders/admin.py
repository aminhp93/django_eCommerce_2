from django.contrib import admin

from .models import UserCheckout, UserAddress
# Register your models here.

admin.site.register(UserCheckout)
admin.site.register(UserAddress)
