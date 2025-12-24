from django.urls import path
from .views import EmployerListView, EmployerDetailView, EmployerUpdateView

app_name = "employer"

urlpatterns = [
    path("", EmployerListView.as_view(), name="list"),
    path("<int:pk>/", EmployerDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", EmployerUpdateView.as_view(), name="update"),
]
