from rest_framework import serializers
from .models import Image


class CreateImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['image']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image', 'small_thumbnail', 'big_thumbnail']


class BaseAccountImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['small_thumbnail']
