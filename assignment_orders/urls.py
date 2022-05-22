from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from assignment_orders.endpoints import ProductsView, PlaceOrderView, RetrieveUserOrders, CalcOrderPrice, UserModViewSet

router = DefaultRouter()

router.register(r'api/user', UserModViewSet, basename="user")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('auth', TokenObtainPairView.as_view(), name="token_authorization"),
        path('refresh', TokenRefreshView.as_view(), name="token_refresh"),
        path('products', ProductsView.as_view(), name="products"),
        path('order', PlaceOrderView.as_view(), name="place_order"),
        path('calc', CalcOrderPrice.as_view(), name="calc_order_price"),
        path('my-orders', RetrieveUserOrders.as_view(), name="user_orders"),
    ]))
] + router.urls
