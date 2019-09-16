import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout

# Create your views here.
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        user = authenticate(
            username=request.data.get("username"), password=request.data.get("password")
        )
        if user is not None:
            login(request, user)
            return Response("", status=status.HTTP_200_OK)
        return Respone("User not found", status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        print(request.user)
        print(request.user.is_authenticated)
        logout(request)
        return Response("", status=status.HTTP_200_OK)


class SessionCheckView(APIView):
    permission_classes = []

    def get(self, request):
        print(request.user)
        print(request.user.is_authenticated)
        return Response(
            json.dumps({"is_authenticated": request.user.is_authenticated}),
            status=status.HTTP_200_OK,
        )
