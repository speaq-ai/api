from message.views import MessageView
from django.urls import path

from . import views

urlpatterns = [path("", MessageView.as_view()),
               path('search/<string:query>/', views.kaggle_search)]
