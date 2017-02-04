from django.contrib import admin

from .models import Product, Variation, ProductImage
# Register your models here.

admin.site.register(Product)
admin.site.register(Variation)
admin.site.register(ProductImage)
