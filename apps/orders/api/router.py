from rest_framework.routers import DefaultRouter
from django.urls import path
from .viewsets import GetTodayOrders, GetOrdersByItem, GetOrdersByUser, GetOrderDetails, GetOrderByDate, OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='The orders viewset')
router.register('order_item', OrderItemViewSet, basename='The order item viewset')

urlpatterns = [
    path('get_order_details/<int:order_id>/', GetOrderDetails.as_view(), name="order_details"),
    path('get_today_orders/', GetTodayOrders.as_view(), name="todays_orders"),
    path('get_orders_by_item/<str:product_name>/', GetOrdersByItem.as_view(), name="order_by_item"),
    path('get_orders_by_date/', GetOrderByDate.as_view(), name="order_by_date"),
    path('get_orders_by_user/<int:user_id>',GetOrdersByUser.as_view(), name="orders_by_user"),
] + router.urls
