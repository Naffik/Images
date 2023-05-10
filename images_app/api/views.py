from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ImageSerializer
from user_app.models import User
from images_app.models import Image


class CreateImageView(generics.CreateAPIView):
    permissions_classes = [IsAuthenticated]
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class ListImageView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
