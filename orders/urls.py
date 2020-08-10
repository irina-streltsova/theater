from django.urls import path
from . import views

urlpatterns = [
    path("", views.order_create, name="order_create"),
    path("my-orders/", views.my_orders, name="my_orders"),
]