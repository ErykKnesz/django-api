from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Image
from .serializers import ImageSerializer
from .permissions import IsAuthenticatedAndOwner


class ImageList(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticatedAndOwner]

    def get_queryset(self):
        queryset = Image.objects.filter(owner=self.request.user.id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = Response(serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        return response

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ImageDetail(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticatedAndOwner]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        return Response(serializer.data)

