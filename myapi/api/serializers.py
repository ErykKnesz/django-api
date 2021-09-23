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


class LinkSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Image
        fields = ('image_url',)

    def get_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj)
