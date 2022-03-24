from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from assignment_orders.models import Product, Order
from assignment_orders.serializers import ProductSerializer, OrderSerializer, PlaceOrderSerializer


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
        if not data.is_valid():
            return JsonResponse(dict(data.errors), status=400)
        res = data.save()
        return JsonResponse(data=res, status=201)


class RetrieveUserOrders(APIView):
    """
    Session-based endpoint to retrieve a list of user's orders
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self, request):
        return JsonResponse(
            self.serializer_class(Order.objects.filter(user=request.user), many=True).data,
            safe=False
        )
