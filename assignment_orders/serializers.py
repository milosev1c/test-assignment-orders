from rest_framework.serializers import ModelSerializer
from assignment_orders.models import Product, Order, OrderPart
from django.conf import settings


class ProductSerializer(ModelSerializer):
    """
    Products serializer
    """
    class Meta:
        model = Product
        fields = "__all__"
