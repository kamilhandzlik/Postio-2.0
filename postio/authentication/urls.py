from django.urls import path, include
from .views import CustomLoginView, CustomLogoutView, RegistrationView

urlpatterns = [
 path('login/', CustomLoginView.as_view(), name='login'),
 path('logout/', CustomLogoutView.as_view(), name='logout'),
 path('register/', RegistrationView.as_view(), name='register')
]