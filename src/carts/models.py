from decimal import Decimal

from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save

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

class Cart(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	items = models.ManyToManyField(Variation, through=CartItem)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return str(self.id)
