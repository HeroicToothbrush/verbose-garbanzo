# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product, Order, InvalidOrderError, NotEnoughStockError


class OrderTestCase(TestCase):
    """
    Tests for the business logic as specified - checking that a given quantity is greater than zero, that
    stock levels are sufficient, stock quantities are updated when ordered and that order price is calculated correctly.
    """

    def setUp(self):
        Product.objects.create(name="Peanuts", price=3.78, stock_qty=5)
        self.user = User.objects.create(username="testuser")
        self.product = Product.objects.get(name="Peanuts")

    def test_invalid_qty_order(self):
        order = Order(user=self.user, product=self.product, qty=0)
        with self.assertRaises(InvalidOrderError):
            order.save()

    def test_insufficient_stock(self):
        order = Order(user=self.user, product=self.product, qty=6)
        with self.assertRaises(NotEnoughStockError):
            order.save()

    def test_stock_qty_updates(self):
        order = Order(user=self.user, product=self.product, qty=3)
        order.save()
        self.assertEqual(2, self.product.stock_qty)

    def test_order_price(self):
        order = Order(user=self.user, product=self.product, qty=3)
        order.save()
        self.assertEqual(11.34, float(order.cost))