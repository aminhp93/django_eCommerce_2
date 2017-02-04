from django.views.generic import DetailView, ListView
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone

# Create your views here.
from .models import Product

class ProductListView(ListView):
	model = Product
	# queryset = Product.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data()
		print(context)
		context["now"] = timezone.now
		return context

class ProductDetailView(DetailView):
	model = Product

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