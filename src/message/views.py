import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from message.utils import AssistantAPI
from users.models import Profile
from users.serializers import ProfileSerializer

# Create your views here.
class MessageView(APIView):
    def post(self, request):
        message_text = request.data.get("inputText")
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = ProfileSerializer(data={"user": request.user}).save()

        if profile.assistant_session:
            assistant_session = profile.assistant_session
        else:
            assistant_session = AssistantAPI.create_session()
            profile.assistant_session = assistant_session
            profile.save()
        assistant_api = AssistantAPI(assistant_session)

        data = assistant_api.message(message_text)
        return Response(json.dumps(data), status=status.HTTP_200_OK)
