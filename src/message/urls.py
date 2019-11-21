from message.views import MessageView
from django.urls import path

from . import views

urlpatterns = [path("", MessageView.as_view()),
               path('search/', views.kaggle_search)]
