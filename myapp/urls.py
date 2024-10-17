from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    ClientListCreateAPIView,
    ClientDetailAPIView,
    ProjectCreateAPIView,
    UserProjectsAPIView,
)


urlpatterns = [
    path('clients/', ClientListCreateAPIView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientDetailAPIView.as_view(), name='client-detail'),
    path('clients/<int:client_id>/projects/', ProjectCreateAPIView.as_view(), name='project-create'),
    path('projects/', UserProjectsAPIView.as_view(), name='user-projects'),
     # User registration and login
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
]
