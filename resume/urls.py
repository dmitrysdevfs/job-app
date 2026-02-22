from django.urls import path
from . import views

app_name = 'resume'

urlpatterns = [
    path('', views.ResumeListView.as_view(), name='list'),
    path('browse/', views.PublicResumeListView.as_view(), name='browse'),
    path('create/', views.ResumeCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ResumeDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ResumeUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ResumeDeleteView.as_view(), name='delete'),
    path('<int:pk>/request-contact/', views.RequestContactView.as_view(), name='request_contact'),
    path('contact-request/<int:pk>/approve/', views.ApproveContactRequestView.as_view(), name='approve_request'),
    path('contact-request/<int:pk>/reject/', views.RejectContactRequestView.as_view(), name='reject_request'),
]
