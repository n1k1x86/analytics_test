from django.urls import path
from .views import LoginView, LogoutView, sign_up

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('register/', sign_up)
]