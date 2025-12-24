from django.urls import path
from .views import EmployerListView

app_name = "employer"

urlpatterns = [
    path("", EmployerListView.as_view(), name="list"),
]
