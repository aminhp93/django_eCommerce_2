from django.contrib import admin

from .models import Product, Variation, ProductImage, Category, ProductFeatured
# Register your models here.

admin.site.register(Product)
admin.site.register(Variation)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(ProductFeatured)
