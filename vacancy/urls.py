from django.urls import path
from . import views

app_name = 'vacancy'

urlpatterns = [
    path("", views.vacancy_list, name="list"),
    path("<int:pk>/", views.vacancy_detail, name="detail"),
]
