import random

from django.contrib import messages
from django.db.models import Q
from django.views.generic import DetailView, ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone

# Create your views here.
from .forms import VariationInventoryFormSet
from .models import Product, Variation, Category
from .mixins import StaffRequiredMixin

class CategoryListView(ListView):
	model = Category
	queryset = Category.objects.all()
	template_name = "products/product_list.html"

class CategoryDetailView(DetailView):
	model = Category
	
	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		obj = self.get_object()
		product_set = obj.product_set.all()
		default_products = obj.default_category.all()
		products = (product_set | default_products).distinct()
		context["products"] = products
		return context

class VariationListView(StaffRequiredMixin, ListView):
	model = Variation
	queryset = Variation.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context["formset"] = VariationInventoryFormSet(queryset=self.get_queryset())
		return context

	def get_queryset(self, *args, **kwargs):	
		product_pk = self.kwargs.get("pk")
		if product_pk:
			product = get_object_or_404(Product, pk = product_pk)
			queryset = Variation.objects.filter(product=product)
		return queryset

	def post(self, request, *args, **kawrgs):
		print(request.POST)
		formset = VariationInventoryFormSet(request.POST, request.FILES)
		if formset.is_valid():
			formset.save(commit=False)
			for form in formset:
				new_item = form.save(commit=False)
				# if new_item.title:
				product_pk = self.kwargs.get("pk")
				product = get_object_or_404(Product, pk=product_pk)
				new_item.product = product
				new_item.save()
			messages.success(request, "Your inventory has been updated")
			return redirect("product_list")
		raise Http404

class ProductListView(ListView):
	model = Product
	# queryset = Product.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data()
		print(context)
		context["now"] = timezone.now
		context["query"] = self.request.GET.get("q")
		return context

	def get_queryset(self, *args, **kwargs):
		qs = super().get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = self.model.objects.filter(
				Q(title__icontains=query) | 
				Q(description__icontains=query)
				)
			try:
				qs2 = self.model.objects.filet(
					Q(price=query)
					)
				qs = (qs | qs2).distinct()
			except:
				pass
		return qs

class ProductDetailView(DetailView):
	model = Product

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		instance = self.get_object()

		context["related"] = sorted(Product.objects.get_related(instance).order_by("title")[:6], key=lambda x: random.random())
		return context

def product_detail_view_func(request, id):
	product_instance = get_object_or_404(Product, id=id)
	# try:
	# 	product_instance = Product.objects.get(id=id)
	# except Product.DoesNotExist:
	# 	raise Http404
	# except:
	# 	raise Http404
	template = "products/product_detail.html"
	context = {
		"object": product_instance
	}
	return render(request, template, context)