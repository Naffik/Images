from django.db import models


class Thumbnail(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(upload_to='images/thumbnails/')


class Image(models.Model):
    original_image = models.ImageField(upload_to='images/original/')