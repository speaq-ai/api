from django.urls import path
from users.views import LoginView, LogoutView, SessionCheckView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("check/", SessionCheckView.as_view()),
]
