from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from assignment_orders.models import Product, Order
from assignment_orders.permissions import IsAdminOrMe
from assignment_orders.serializers import ProductSerializer, OrderSerializer, PlaceOrderSerializer, FullUserSerializer, \
    BasicUserSerializer, PasswordSerializer


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

    def get_queryset(self):
        filter_map = {
            "name": "name__icontains",
            "price__gte": "price__gte",
            "price__lte": "price__lte",
            "quantity": "quantity__gte"
        }
        product_filter = {}
        for key, value in filter_map.items():
            if key in self.request.GET:
                product_filter[value] = self.request.GET.get(key)
        if "in_stock" in self.request.GET:
            if self.request.GET.get("in_stock") == "true":
                product_filter["quantity__gt"] = 0
            else:
                product_filter["quantity"] = 0

        return self.queryset.filter(**product_filter)


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


class CalcOrderPrice(APIView):
    """
    Quick lookup for order price without placing an order
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        :param request: GET request, should contain 'product' list
        :return: JSON response
        """
        products = request.GET.getlist('product')
        if not products:
            return JsonResponse({"product": "'product' should have at least one element"}, status=400)
        price = Product.objects.filter(
            id__in=request.GET.getlist("product")
        ).aggregate(summary=Sum("price"))
        return JsonResponse(price)


class UserModViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in ("list", "create"):
            permission_classes = [IsAdminUser]
        if self.action in ("retrieve", "update", "partial_update", "destroy", "change_password"):
            permission_classes = [IsAdminOrMe]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Different serializers for staff and users
        """
        if self.request.user.is_staff:
            return FullUserSerializer
        return BasicUserSerializer

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        user = get_user_model().objects.get(pk=pk)
        data = PasswordSerializer(data=request.data, request=request, user=user)
        if data.is_valid():
            return JsonResponse({'status': 'password set'})
        else:
            return JsonResponse(dict(data.errors), status=400)
