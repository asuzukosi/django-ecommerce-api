from rest_framework.serializers import ModelSerializer
from apps.orders.models import Order, OrderItem


class OrderSummarySerializer(ModelSerializer):
    """
    This is a serializer for the Order model
    this serializer gives a brief summary of the order
    """
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(ModelSerializer):
    """
    This is a serializer of the OrderItem model
    This provides the details of the order item
    """
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderDetailedSerializer(ModelSerializer):
    """
    This is a serializer of the Order model
    This gives all the details of the order and all
    it's order items
    """
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
