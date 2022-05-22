from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from assignment_orders.models import Product, Order, OrderPart


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
        if not self.context["request"].data["parts"]:
            raise ValidationError({"parts": "Order must contain at least one product in 'parts' field"})
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


class FullUserSerializer(ModelSerializer):
    """
    Extended Serializer for User model
    """
    class Meta:
        model = get_user_model()
        exclude = ("password",)
        readonly_field = "date_joined", "username", "last_login", "id"


class BasicUserSerializer(ModelSerializer):
    """
    Basic serializer for users only
    """
    class Meta:
        model = get_user_model()
        exclude = ("password", "is_active", "is_staff", "is_superuser")
        readonly_field = "date_joined", "username", "last_login", "groups", "user_permissions"


class PasswordSerializer(Serializer):
    username_validator = UnicodeUsernameValidator()
    old_password = CharField(max_length=128, write_only=True)
    new_password = CharField(max_length=128, write_only=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.user = kwargs.pop("user")
        super(PasswordSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        old_password = data.get("old_password", None)
        new_password = data.get("new_password", None)

        user = authenticate(self.request, username=self.user.username, password=old_password)

        if user is None:
            raise ValidationError("Old password is not valid")

        if not user.is_active:
            raise ValidationError("This user has been deactivated")

        user.set_password(new_password)
        user.save()

        return {
            "user": user,
            "email": user.email,
            "username": user.username,
        }


