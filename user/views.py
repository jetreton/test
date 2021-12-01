from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import *


class RegisterView(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfully registered!', 200)


class ActivationView(APIView):
    
    def get(self, request, email, activation_code):
        user = User.objects.filter(
            email=email,
            activation_code=activation_code
        ).first()
        if not user:
            return Response('User does not exist', 400)
        user.is_active = True
        user.save()
        return Response('Successfully activated!', 200)