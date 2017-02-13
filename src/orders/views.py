from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from .forms import AddressForm, UserAddressForm
from .models import UserAddress, UserCheckout, Order
from .mixins import CartOrderMixin, LoginRequiredMixin
# Create your views here.

class OrderList(LoginRequiredMixin, ListView):
	queryset = Order.objects.all()

	def get_queryset(self):
		user_checkout_id = self.request.user.id
		user_checkout = UserCheckout.objects.get(id=user_checkout_id)
		return super().get_queryset().filter(user=user_checkout)

class UserAddressCreateView(CreateView):
	form_class = UserAddressForm
	template_name = "forms.html"
	success_url = "/checkout/address/"

	def get_checkout_user(self):
		user_checkout_id = self.request.session.get("user_checkout_id")
		user_checkout = UserCheckout.objects.get(id=user_checkout_id)
		return user_checkout

	def form_valid(self, form, *args, **kwargs):
		form.instance.user = self.get_checkout_user()
		return super().form_valid(form, *args, **kwargs)

class AddressSelectFormView(CartOrderMixin, FormView):
	form_class = AddressForm
	template_name = "orders/address_select.html"

	def dispatch(self, *args, **kwargs):
		b_address, s_address = self.get_addresses()
		print("20", b_address)

		if b_address.count() == 0:
			messages.success(self.request, "Please add a billing address befefore continuing")
			return redirect("order_address_create")
		elif s_address.count() == 0:
			messages.success(self.request, "Please add a shippin address befefore continuing")
			return redirect("order_address_create")
		else:
			return super().dispatch(*args, **kwargs)

	def get_addresses(self, *args, **kwargs):
		user_checkout_id = self.request.session.get("user_checkout_id")
		user_checkout = UserCheckout.objects.get(id=user_checkout_id)
		b_address = UserAddress.objects.filter(
				user=user_checkout,
				type="billing",
			)

		s_address = UserAddress.objects.filter(
				user=user_checkout,
				# user__email=self.request.user.email,
				type="shipping",
			)
		return b_address, s_address

	def get_form(self, *args, **kwargs):
		form = super().get_form(*args, **kwargs)
		b_address, s_address = self.get_addresses()

		form.fields["billing_address"].queryset = b_address
		form.fields["shipping_address"].queryset = s_address

		return form

	def form_valid(self, form, *args, **kwargs):
		billing_address = form.cleaned_data["billing_address"]
		shipping_address = form.cleaned_data["shipping_address"]
		order = self.get_order()
		order.billing_address = billing_address
		order.shipping_address = shipping_address
		order.save()

		return super().form_valid(form, *args, **kwargs)

	def get_success_url(self, *args, **kwags):
		return "/checkout/"


