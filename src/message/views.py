import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from message.utils.AssistantAPI import AssistantAPI
from users.models import Profile
from users.serializers import ProfileSerializer
from message.utils.kaggle import list_datasets

class SearchView(APIView):
    def post(self, request):
    # pass the query to the functions that Jamie defines here
        datasets = list_datasets(max_size = 5000, file_type="csv", search = request.data.get("query"))

        # check serialization
        return Response(json.dumps(datasets), status=status.HTTP_200_OK)

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
        data["input_text"] = message_text
        if config.get("outputAsSpeech"):
            data["speech"] = assistant_api.text_to_speech(data["text"])

        return Response(json.dumps(data), status=status.HTTP_200_OK)
