from django.urls import path
from .views import RegisterView, CurrentUserProfileView, ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path("profile/", CurrentUserProfileView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
]
