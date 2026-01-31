from django.urls import path
from . import views

app_name = 'resume'

urlpatterns = [
    path('', views.ResumeListView.as_view(), name='list'),
    path('create/', views.ResumeCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.ResumeUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ResumeDeleteView.as_view(), name='delete'),
]
