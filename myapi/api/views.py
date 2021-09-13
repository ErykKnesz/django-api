from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import (api_view,
                                       permission_classes)
from request_token.models import RequestToken
from request_token.decorators import use_request_token
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.http import FileResponse
from django.urls import reverse

from .models import Image
from .serializers import (CreateImageSerializer, ImageSerializer,
                          BaseAccountImageSerializer, LinkSerializer)
from .permissions import IsAuthenticatedAndOwner, HasExpiringLinks


class CreateImage(generics.CreateAPIView):
    serializer_class = CreateImageSerializer
    permission_classes = [IsAuthenticatedAndOwner]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_instance = self.perform_create(serializer)
        if self.request.user.account.is_base():
            instance_serializer = BaseAccountImageSerializer(
                serializer_instance, context={'request': request})
        else:
            instance_serializer = ImageSerializer(serializer_instance)
        headers = self.get_success_headers(instance_serializer.data)
        response = Response(instance_serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        return response


class ImageList(generics.ListAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticatedAndOwner]

    def get_queryset(self):
        queryset = Image.objects.filter(user=self.request.user.id)
        return queryset

    def list(self, request, *args, **kwargs):
        if self.request.user.account.is_base():
            self.serializer_class = BaseAccountImageSerializer
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ImageDetail(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticatedAndOwner]

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.account.is_base():
            self.serializer_class = BaseAccountImageSerializer
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@api_view(http_method_names=['GET'])
@permission_classes((IsAuthenticatedAndOwner, HasExpiringLinks))
def create_expiring_link(request, pk, life):
    token = RequestToken.objects.create_token(
        scope="link",
        login_mode=RequestToken.LOGIN_MODE_NONE,
        data={'img_id': pk}
    )
    if life < 30 or life > 30000:
        msg = "Token life needs to be within the range of 30 to 30 000 seconds."
        return Response(msg, status=400)
    token.expiration_time = timezone.now() + timezone.timedelta(seconds=life)
    token.save()
    url = reverse('display_image', args=[pk])
    serializer = LinkSerializer(url, context={"request": request})
    image_url = serializer.data['image_url']
    data = {'expiring link': image_url + '?rt=' + token.jwt(),
            'claims': token.claims}
    return Response(data, status=200)


@api_view(http_method_names=['GET'])
@permission_classes((AllowAny,))
@use_request_token(scope="link", required=False)
def handle_expiring_link(request, pk):
    print(request.token)
    img_id = (
        request.token.data['img_id']
        if hasattr(request, 'token')
        else None
    )
    img = Image.objects.get(pk=img_id)
    return FileResponse(open(img.image.path, 'rb'))