from message.views import MessageView
from django.urls import path

urlpatterns = [path("", MessageView.as_view())]
