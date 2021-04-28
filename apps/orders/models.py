from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Order(models.Model):
    """
    This is a model to store users order and keep
    track of previous orders
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    amount = models.FloatField()
    discount = models.BooleanField(default=False)
    address = models.TextField()
    zip_code = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    time_of_order = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_of_order', ]

    def __str__(self):
        """
        Prints out the string name of an entire order
        eg
        :return:string
        """
        return f"{self.user.last_name} {self.user.first_name} on {self.time_of_order} amount {self.amount}"


class OrderItem(models.Model):
    """
    This is a single item that was ordered in an entire order list
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, null=True)
    individual_price = models.FloatField()
    quantity = models.IntegerField()

    def __str__(self):
        """
        Prints out the string name of a single order item
        eg: 8 shoe's in order by Asuzu Kosi on 19/ 2/ 2021 amount $2000
        :return: string
        """
        return f"{self.quantity} {self.name}'s in order by {self.order}"

    def compute_amount(self):
        """
        This returns the total amount for the purchase of this item
        :return: float
        """
        return int(self.quantity) * float(self.individual_price)
