from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from user_app.api.serializers import RegistrationSerializer, UserSerializer
from user_app.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class RegistrationView(generics.GenericAPIView):
    """
    Create new User with POST data

    -username
    -email
    -password
    -password2
    """
    serializer_class = RegistrationSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve/Update/Destroy ViewSet for User model
    """
    serializer_class = UserSerializer

    def get_object(self):
        return User.objects.get(username=self.kwargs.get('username'))


class UserListView(generics.ListAPIView):
    """
    List ViewSet for User model
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
