from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from .models import Image, User
from .serializers import ImageSerializer
from .permissions import IsOwner


class ImageList(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        queryset = Image.objects.filter(owner=self.request.user.id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res_content = serializer.data['name'] # TO BE AMENDED!
        return Response(res_content, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


def thumbnail_200(request, queryset):
    thumbnail = queryset.set_thumbnails(queryset, request.user)
    return thumbnail


class ImageDetail(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsOwner]

    def retrieve(self, *args, **kwargs):
        instance = self.get_object()
        t = thumbnail_200(self.request, instance)
        serializer = self.get_serializer(t)
        serializer.name = instance.name
        serializer.owner = instance.owner
        return Response(instance.name)


