from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormMixin

from carts.models import Cart, CartItem
from orders.forms import GuestCheckoutForm
from orders.models import UserCheckout, UserAddress
from products.models import Variation
# Create your views here.

class ItemCountView(View):
	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			cart_id = self.request.session.get("cart_id")
			if cart_id == None:
				count = 0
			else:
				cart = Cart.objects.get(id=cart_id)
				count = cart.items.count()
			request.session["cart_item_count"] = count
			return JsonResponse({"count": count})
		else:
			raise Http404


class CartView(SingleObjectMixin, View):
	model = Cart 
	template_name = "carts/view.html"

	def get_object(self, *args, **kwargs):
		# request.session.set_expiry(300) # 5 minutes
		cart_id = self.request.session.get("cart_id")
		if cart_id == None:
			cart = Cart()			
			cart.save()
			cart_id = cart.id
			self.request.session["cart_id"] = cart_id
		cart = Cart.objects.get(id=cart_id)
		cart.tax_percentage = 0.075
		if self.request.user.is_authenticated():
			cart.user = self.request.user
			cart.save()
		return cart

	def get(self, request, *args, **kwargs):
		cart = self.get_object()
		item_id = request.GET.get("item")
		delete_item = request.GET.get("delete", False)
		item_added = False
		flash_message = ""

		if item_id:
			item_instance = get_object_or_404(Variation, id=item_id)
			quantity = request.GET.get("quantity", 1)
			try:
				if int(quantity) < 1:
					delete_item = True
			except:
				raise Http404

			cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
			
			if created:
				flash_message = "Successfully added to the cart"
				item_added = True
			if delete_item:
				flash_message = "Item removed successfully"
				cart_item.delete()
			else:
				if not created:
					flash_message = "Quantity has been updated successfully"
				cart_item.quantity = quantity
				cart_item.save()
			if not request.is_ajax():
				return HttpResponseRedirect(reverse("carts"))
				# return cart_item.cart.get_absolute_url()

			
		if request.is_ajax():
			try:
				total = cart_item.line_item_total
			except:
				total = None

			try:
				subtotal = cart_item.cart.subtotal
			except:
				subtotal = None

			try:
				cart_total = cart_item.cart.total
			except:
				cart_total = None

			try:
				tax_total = cart_item.cart.tax_total
			except:
				tax_total = None

			try:
				total_items = cart_item.cart.items.count()
			except:
				total_items = 0
				
			data = {
				"delete": delete_item, 
				"item_added": item_added,
				"line_total": total,
				"subtotal": subtotal,
				"cart_total": cart_total,
				"tax_total": tax_total,
				"flash_message": flash_message,
			}
			return JsonResponse(data)

		context = {
			"object": self.get_object()
		}
		template = self.template_name
		return render(request, template, context)

class CheckoutView(FormMixin, DetailView):
	model = Cart
	template_name = "carts/checkout_view.html"
	form_class = GuestCheckoutForm

	def get_object(self, *args, **kwargs):
		cart_id = self.request.session.get("cart_id")
		if cart_id == None:
			return redirect("carts")
		cart = Cart.objects.get(id=cart_id)
		cart.tax_percentage = 0.075
		if self.request.user.is_authenticated():
			cart.user = self.request.user
			cart.save()
		return cart


	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		user_can_continue = False
		user_checkout_id = self.request.session.get("user_checkout_id")

		if not self.request.user.is_authenticated() or user_checkout_id == None: #or if self.request.user.is_guest
			context["login_form"] = AuthenticationForm()
			context["next_url"] = self.request.build_absolute_uri()
		if self.request.user.is_authenticated() or user_checkout_id != None:
			user_can_continue = True

		if self.request.user.is_authenticated():
			user_checkout, created = UserCheckout.objects.get_or_create(email=self.request.user.email)
			user_checkout.user = self.request.user
			user_checkout.save()
			self.request.session["user_checkout_id"] = user_checkout.id

		
		context["user_can_continue"] = user_can_continue
		context["form"] = self.get_form()
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form()
		
		if form.is_valid():
			email = form.cleaned_data.get("email")
			user_checkout, created = UserCheckout.objects.get_or_create(email=email)
			request.session["user_checkout_id"] = user_checkout.id
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse("checkout")

	def get(self, request, *args, **kwargs):
		get_data = super().get(request, *args, **kwargs)
		cart = self.get_object()

		user_checkout_id = request.session.get("user_checkout_id")
		if user_checkout_id != None:
			user_checkout = UserCheckout.objects.get(id=user_checkout_id)

		user = user_checkout

		billing_address_id = request.session.get("billing_address_id")
		shipping_address_id = request.session.get("shipping_address_id")

		if billing_address_id == None or shipping_address_id == None:
			return redirect("order_address")
		else:
			billing_address = UserAddress.objects.get(id=billing_address_id)
			shipping_address = UserAddress.objects.get(id=shipping_address_id)

		try:
			new_order_id = request.session["order_id"]
			new_order = Order.objects.get(id=new_order_id)
		except:
			new_order = Order()
			request.session["order_id"] = new_order.id

		new_order = Order()
		new_order.cart = cart
		new_order.user = user
		new_order.billing_address = billing_address
		new_order.shipping_address = shipping_address
		new_order.save()


