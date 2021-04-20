from django.urls import path
from . import views


urlpatterns = [
    path('images/', views.ImageList.as_view(), name='image_list'),
    path('images/<int:pk>/',
         views.ImageDetail.as_view(),
         name='image-details'),
    path('images/<int:pk>/thumbnail200/',
         views.thumbnail_200,
         name='thumbnail200'),
    path('images/<int:pk>/thumbnail400/',
         views.thumbnail_400,
         name='thumbnail400'),
]