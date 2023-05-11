from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ImageSerializer
from user_app.models import User
from images_app.models import Image

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class CreateImageView(generics.CreateAPIView):
    permissions_classes = [IsAuthenticated]
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        if 'original_image' not in request.FILES:
            raise ValidationError('File not uploaded')
        file = request.FILES['original_image']

        try:
            if not allowed_file(file.name):
                raise ValidationError('File extension not allowed')
        except DjangoValidationError:
            raise ValidationError('Incorrect file')

        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class ListImageView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSerializer

    def get_queryset(self):
        user = self.request.user
        return Image.objects.all().filter(user=user)


class FetchExpiringLinkView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
