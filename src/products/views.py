from django.db.models import Q
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