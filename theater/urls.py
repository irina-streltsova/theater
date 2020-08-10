from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:performance_id>", views.performance, name="performance"),
    path("booking/<int:performance_id>", views.ticket_selection, name="ticket_selection")
]