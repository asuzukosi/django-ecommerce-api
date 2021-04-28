from abc import ABC

from rest_framework.views import APIView
from .serializer import OrderItemSerializer, OrderSummarySerializer, OrderDetailedSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from apps.orders.models import Order, OrderItem
import datetime


class GetOrdersByUser(APIView):
    """
    This is an API View to get all the orders
    of the user with the specified id
    """
    def get(self, request, user_id):
        """
        This is the get method of the get orders by user endpoint
        :param request:
        :param user_id:
        :return: json response
        """
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return Response({
                "message": "User with specified id does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)
        orders = user.orders

        serializer = OrderSummarySerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DateRequestSerializer(serializers.Serializer):
    """
    This is a serializer class used for retrieving dates in a post request
    it is used in the GetOrderByDate api view
    """
    date = serializers.DateTimeField()


class GetOrderByDate(APIView):
    """
    This is an api endpoint to get all the
    orders of a specific day
    """
    def post(self, request):
        """
        This is the post request of the get order by date endpoint it takes in
        a json body parameter
        :param request:
        :return: json response
        """

        serializer = DateRequestSerializer(request.body)
        if serializer.is_valid():
            date = serializer.data['date']
            orders = Order.object.filter(time_of_order=date)
            serializer = OrderSummarySerializer(orders, many=True)

            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({
                "message": "Invalid request body format"
            }, status.HTTP_400_BAD_REQUEST)


class GetOrdersByItem(APIView):
    """
    This is an api request to get all
    orders that have a specific item
    """
    def get_orders_by_item_name(self, product_name):
        """
        This will return all the orders that have an order item with the
        specified product_name
        :param product_name:
        :return: list of order instances
        """
        orders = set()
        order_items = OrderItem.objects.filter(name=product_name)

        # Get all the orders of the order items and store them in a set
        for order_item in order_items:
            orders.add(order_item.order)

        return list(orders)

    def get(self, product_name):
        """
        This is the get request for the get order by name endpoint
        :param product_name:
        :return: JSON response
        """
        orders = self.get_orders_by_item_name(product_name)
        serializer = OrderSummarySerializer(orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTodayOrders(APIView):
    """
    This is an API endpoint to get all the
    orders that took place today
    """
    def get(self):
        """
        This is the get method for the get today's orders endpoint
        :return: Json response
        """
        orders = Order.object.filter(time_of_order__date=datetime.date.today())

        serializer = OrderSummarySerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetOrderDetails(APIView):
    """
    This is an api endpoint to retrieve the full details of an order
    and all it's order items
    """

    def get(self, order_id):
        """
        This is the get request to get an orders details
        :param order_id:
        :return: Json response
        """
        order = Order.object.get(pk=order_id)
        serializer = OrderDetailedSerializer(instance=order)

        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderViewSet(ModelViewSet):
    """
    This is the viewset for the Order Model
    it has endpoint for get, post, put, patch and delete
    """
    serializer_class = OrderSummarySerializer
    queryset = Order.objects.all()


class OrderItemViewSet(ModelViewSet):
    """
    This is the viewset for the Order Items Model
    it has endpoint for get, post, put, patch and delete
    """
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()



