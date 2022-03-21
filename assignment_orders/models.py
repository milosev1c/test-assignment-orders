from django.db.models import Model, CharField, IntegerField, FloatField, PositiveIntegerField, ManyToManyField, \
    ForeignKey, CASCADE, SET_NULL

from django.conf import settings

"""
Overall – users will be objects of standard Django User model
"""


class Product(Model):
    """
    Product model with name, price and quantity as positive number
    """
    name = CharField(max_length=255, verbose_name="Name")
    price = FloatField(verbose_name="Price")
    quantity = PositiveIntegerField(verbose_name="Quantity in stock")


class OrderPart(Model):
    """
    Order part, holds information about product and quantity in order
    Field 'product_name' is fallback for displaying products removed from database
    """
    product = ForeignKey(to=Product, on_delete=SET_NULL, null=True, verbose_name="Product")
    product_name = CharField(max_length=255, verbose_name="Product name")
    quantity_in_order = PositiveIntegerField(verbose_name="Quantity in order")


class Order(Model):
    """
    Order itself, has a link to user and M2M relation to order parts
    """
    user = ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="orders")
    parts = ManyToManyField(OrderPart)

