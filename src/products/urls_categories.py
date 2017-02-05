from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .views import CategoryListView, CategoryDetailView

urlpatterns = [
	url(r'^$', CategoryListView.as_view(), name='categories'),
	url(r'^(?P<slug>[\w-]+)/$', CategoryDetailView.as_view(), name='category_detail'),

]