from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .views import product_detail_view_func, ProductDetailView, ProductListView, VariationListView

urlpatterns = [
	url(r'^$', ProductListView.as_view(), name='product_list'),
    url(r'^(?P<pk>\d+)$', ProductDetailView.as_view(), name='product_detail'),
    url(r'^(?P<pk>\d+)/inventory/$', VariationListView.as_view(), name='product_inventory'),
    # url(r'^(?P<id>\d+)$', product_detail_view_func, name='product_detail_view_func'),
    
]