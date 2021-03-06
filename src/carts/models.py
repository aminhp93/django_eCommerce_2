from decimal import Decimal

from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete

from products.models import Variation

# Create your models here.
class CartItem(models.Model):
	cart = models.ForeignKey("Cart")
	item = models.ForeignKey(Variation)
	quantity = models.PositiveIntegerField(default=1)
	line_item_total = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.item.title

	def remove(self):
		# return "{}?item={}&delete=True".format(reverse("carts"), self.item.id)
		return self.item.remove_from_cart()

	def get_title(self):
		return "{} {}".format(self.item.product.title, self.item.title)

def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
	quantity = Decimal(instance.quantity)
	if quantity >= 1:
		print(quantity)
		price = instance.item.get_price()
		line_item_total = quantity * Decimal(price)
		instance.line_item_total = line_item_total

pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)

def cart_item_post_save_receiver(sender, instance, *args, **kawrgs):
	instance.cart.update_subtotal()

post_save.connect(cart_item_post_save_receiver, sender=CartItem)

post_delete.connect(cart_item_post_save_receiver, sender=CartItem)

class Cart(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	items = models.ManyToManyField(Variation, through=CartItem)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	subtotal = models.DecimalField(max_digits=50, decimal_places=2, default=0)
	tax_percentage = models.DecimalField(max_digits=50, decimal_places=2, default=0.085)
	tax_total = models.DecimalField(max_digits=50, decimal_places=2, default=0)
	total = models.DecimalField(max_digits=50, decimal_places=2, default=0)

	def __str__(self):
		return str(self.id)

	def update_subtotal(self):
		subtotal = 0
		items = self.cartitem_set.all()
		for item in items:
			subtotal += item.line_item_total
		self.subtotal = subtotal
		self.save()

def do_tax_and_total_receiver(sender, instance, *args, **kwargs):
	subtotal = instance.subtotal
	tax_total = round(subtotal * Decimal(instance.tax_percentage), 2)
	total = round(subtotal + tax_total, 2)
	instance.tax_total = "{}".format(tax_total, '.2f')
	instance.total = "{}".format(total, '.2f')

pre_save.connect(do_tax_and_total_receiver, sender=Cart)
