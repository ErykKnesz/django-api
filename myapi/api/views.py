from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.shortcuts import render
from .models import Image, User
from .serializers import ImageSerializer
from .permissions import IsOwner
from .thumbnails import create_thumbnail_200, create_thumbnail_400


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


class ImageDetail(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsOwner]

    def retrieve(self, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        link_t_200 = reverse('thumbnail200', args=[instance.id], request=self.request)
        if user.is_premium():
            #t_400 = create_thumbnail_400(instance, self.request)
            link_t_400 = reverse('thumbnail400',args=[instance.id], request=self.request)
            return Response(link_t_400)
        #serializer = self.get_serializer(t)
        #serializer.name = instance.name
        #serializer.owner = instance.owner
        return Response(link_t_200)


def thumbnail_200(request, pk=id):
    instance = Image.objects.get(pk=pk)
    context = {
            'thumbnails': create_thumbnail_200(instance)
        }
    return render(request,'thumbnail200.html', context=context)


def thumbnail_400(request, pk=id):
    context = {
        'thumbnails': create_thumbnail_400()
    }
    return render(request, 'thumbnail400.html', context=context)