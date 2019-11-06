import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from message.utils.AssistantAPI import AssistantAPI
from users.models import Profile
from users.serializers import ProfileSerializer


class MessageView(APIView):
    def post(self, request):
        """
        accepts a JSON request body in the following format:
        {
          "input": <message to send to watson>,
          "config": {
            "inputFormat": "text" | "speech",
            "outputAsSpeech": <boolean>
          }
        }
        """
        message = request.data.get("input", request.data.get("inputText"))
        config = request.data.get("config", {})
        datasets = request.data.get("datasets", [])
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = ProfileSerializer(data={"user": request.user}).save()

        assistant_api = AssistantAPI(profile, datasets)

        if config.get("inputFormat") == "speech":
            mime_type = config.get("mimeType")
            message_text = assistant_api.speech_to_text(message, mime_type)
        else:
            message_text = message

        data = assistant_api.message(message_text)

        if config.get("outputAsSpeech"):
            data["speech"] = assistant_api.text_to_speech(data["text"])

        return Response(json.dumps(data), status=status.HTTP_200_OK)
