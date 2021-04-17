from .models import Image
from .serializers import ImageSerializer
from rest_framework import generics
from .permissions import IsOwner


class ImageList(generics.ListAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        queryset = Image.objects.filter(owner=self.request.user.id)
        return queryset


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    pass