from django.contrib import admin

from .models import Product, Variation
# Register your models here.

admin.site.register(Product)
admin.site.register(Variation)
