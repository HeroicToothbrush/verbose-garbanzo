from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from products.models import Product, Order, InvalidOrderError, NotEnoughStockError
from products.serializers import ProductSerializer, OrderSerializer, UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Products to be viewed, with pagination.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ViewSet):
    """
    API endpoint that allows
    - Orders to be viewed (limited so that a user can only view their own orders)
    - Orders to be created
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()
    product_set = Product.objects.all()

    def list(self, request):
        live_queryset = Order.objects.all().filter(user=request.user)

        serializer_context = {
            'request': request,
        }
        serializer = OrderSerializer(live_queryset, context=serializer_context, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        serializer_context = {
            'request': request,
        }
        order = get_object_or_404(self.queryset, pk=pk, user=request.user)
        serializer = OrderSerializer(order, context=serializer_context)
        return Response(serializer.data)

    def create(self, request):
        # attempt to retrieve product using the ID given in the request and then use this to create an order, \
        # including some basic error handling
        product = get_object_or_404(self.product_set, pk=request.data["product_id"])

        try:
            Order.objects.create(user=request.user, qty=request.data["qty"], product=product)
            return Response({"message": "Successfully created order."}, status=status.HTTP_201_CREATED)
        except InvalidOrderError:
            return Response({"message": "Invalid Order - check request parameters."},
                            status=status.HTTP_400_BAD_REQUEST)
        except NotEnoughStockError:
            return Response({"message": "Failed to create order - not enough stock available"},
                            status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
