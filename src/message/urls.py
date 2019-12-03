from message.views import MessageView
from message.views import SearchView
from django.urls import path

from . import views

urlpatterns = [path("", MessageView.as_view()),
               path('search/', SearchView.as_view())]
