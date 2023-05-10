from rest_framework import serializers
from images_app.models import Image, Thumbnail
from user_app.models import User, AccountTier
from PIL import Image as img
import os
from io import BytesIO


class ThumbnailSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(use_url=True)

    class Meta:
        model = Thumbnail
        fields = ['id', 'name', 'thumbnail']


class ImageSerializer(serializers.ModelSerializer):
    thumbnails = ThumbnailSerializer(many=True, read_only=True)
    original_image = serializers.ImageField(use_url=True)

    class Meta:
        model = Image
        fields = '__all__'

    def create(self, validated_data):
        image = validated_data['original_image']
        image_name, image_extension = os.path.splitext(image.name)
        thumbnail_name = f"{image_name}_thumbnail{image_extension}"
        with img.open(image) as im:
            image_obj = Image.objects.create(**validated_data)
            im.thumbnail((100, 100))
            buffer = BytesIO()
            im.save(buffer, image_extension.replace('.', ''))
            thumbnail_obj = Thumbnail.objects.create(name=thumbnail_name, image=image_obj)
            thumbnail_obj.thumbnail.save(thumbnail_name, buffer)
            print(thumbnail_obj)
        return image_obj

    def to_representation(self, instance):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user is None:
            raise ValueError('request.user is None')

        fields = []
        if not user.account_tier.original_link:
            fields.append('original_image')
        elif not user.account_tier.expiring_link:
            fields.append('expiring_link')
        # else:
        #     fields = ['id', 'name', 'description', 'thumbnail']
        #
        for field_name in set(fields):
            print(field_name)
            self.fields.pop(field_name)

        return super(ImageSerializer, self).to_representation(instance)
