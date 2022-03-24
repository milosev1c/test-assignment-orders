from django.db import transaction
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from assignment_orders.models import Product
from assignment_orders.serializers import ProductSerializer, OrderSerializer, PlaceOrderSerializer
from django.http import JsonResponse


class ProductPaginator(PageNumberPagination):
    """
    Paginator for products
    """
    page_size = 50
    page_size_query_param = 'limit'
    max_page_size = 1000


class ProductsView(ListAPIView):
    """
    Simple paginated products view
    params:
    @page - # of page
    @limit - how many products will be displayed
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPaginator


class PlaceOrderView(APIView):
    """
    Endpoint to create order using existing session
    """
    serializer_class = PlaceOrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = self.serializer_class(data=request.data, context={"request": request})
        data.is_valid()
        res = data.save()
        return JsonResponse(data=res, status=201)
