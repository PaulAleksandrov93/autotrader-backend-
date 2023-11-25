from django.contrib import admin
from django.urls import path, include
from orders.views import order_list, order_detail  # Используем order_list и order_detail из вашего views.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/orders/', order_list, name='order-list'),
    path('api/orders/<int:pk>/', order_detail, name='order-detail'),
]