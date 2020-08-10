from django.urls import path
from . import views

urlpatterns = [
    path("registration", views.register, name="registration"),
    path("authorization", views.authorization, name="authorization"),
    path("", views.dashboard, name="dashboard"),
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("admin-page", views.admin_page, name="admin_page"),
    path("admin/<int:status_id>", views.admin_orders, name="admin_orders"),
    path("admin/execute/<int:order_id>", views.order_execute, name="order_execute"),
    path("admin/complete/<int:order_id>", views.order_complete, name="order_complete"),
    path("admin/reject/<int:order_id>", views.order_reject, name="order_reject")
]