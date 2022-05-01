from django.conf import settings
from django.db import models


class InvalidOrderError(Exception):
    pass


class NotEnoughStockError(Exception):
    pass


class Product(models.Model):

    name = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_qty = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.id} {self.name} {self.price} {self.stock_qty}"


class Order(models.Model):
    ORDER_STATUSES = (
        ('P', 'Pending'),
        ('F', 'Fulfilled'),
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=1, choices=ORDER_STATUSES, default='O')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()

    def save(self, *args, **kwargs):

        """
        Overriden save method validates an order, calculates the cost and updates the stock quantity on the product.
        """

        if not self.qty or self.qty <= 0:
            raise InvalidOrderError

        elif self.product.stock_qty < self.qty:
            raise NotEnoughStockError

        else:

            self.product.stock_qty -= self.qty
            self.cost = self.product.price * self.qty
            self.status = 'P'
            self.product.save()

        return super(Order, self).save(*args, **kwargs)

    def __str__(self):

        return f"{self.id} {self.created} {self.updated} {self.cost} {self.status} {self.product} {self.qty}"
