from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from assignment_orders.endpoints import ProductsView, PlaceOrderView, RetrieveUserOrders

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('auth', TokenObtainPairView.as_view(), name="token_authorization"),
        path('refresh', TokenRefreshView.as_view(), name="token_refresh"),
        path('products', ProductsView.as_view(), name="products"),
        path('order', PlaceOrderView.as_view(), name="place_order"),
        path('my-orders', RetrieveUserOrders.as_view(), name="user_orders")
    ]))
]
