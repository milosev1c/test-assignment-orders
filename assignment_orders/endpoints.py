from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from assignment_orders.models import Product
from assignment_orders.serializers import ProductSerializer


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
