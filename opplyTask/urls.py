from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from products import views
from rest_framework.authtoken import views as auth_view

# register admin, api and authentication routes
router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-token-auth/', auth_view.obtain_auth_token, name='api-token-auth'),
]
