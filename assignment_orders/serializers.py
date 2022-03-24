from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer
from assignment_orders.models import Product, Order, OrderPart
from django.conf import settings


class ProductSerializer(ModelSerializer):
    """
    Products serializer
    """
    class Meta:
        model = Product
        fields = "__all__"


class OrderPartSerializer(ModelSerializer):

    class Meta:
        model = OrderPart
        fields = "product", "quantity_in_order"


class FullOrderPartSerializer(ModelSerializer):
    """
    Serializer only for displaying order part
    """
    class Meta:
        model = OrderPart
        fields = "product", "quantity_in_order", "product_name"


class OrderSerializer(ModelSerializer):
    """
    Serializer for creating an order
    """
    parts = FullOrderPartSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class PlaceOrderSerializer(Serializer):
    """
    Serializer to place order with list of products and their quantity with single transaction.
    If user is trying to order more products than are in stock – the transaction fails
    and the number of products does not change.
    If there are any other errors - it raises validation error.
    """
    @transaction.atomic
    def create(self, validated_data):
        order = OrderSerializer(data={"user": self.context["request"].user.id})
        if not order.is_valid():
            raise ValidationError({"order": order.errors})
        order_obj = order.save()
        new_parts = OrderPartSerializer(data=self.context["request"].data["parts"], many=True)
        new_parts.is_valid()
        for part in new_parts.validated_data:
            part["order"] = order_obj
            part["product_name"] = part["product"].name
            if part["quantity_in_order"] <= part["product"].quantity:
                part["product"].quantity -= part["quantity_in_order"]
                part["product"].save()
            else:
                raise ValidationError({
                    "order_part": "Not enough product in stock to complete the order",
                    "product_id": part["product"].id})

        if not new_parts.is_valid():
            raise ValidationError({"order_part": new_parts.errors})
        new_parts.save()
        return order.data
