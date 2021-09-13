from django.urls import path
from . import views


urlpatterns = [
    path('images/create/', views.CreateImage.as_view(), name='create_image'),
    path('images/', views.ImageList.as_view(), name='image_list'),
    path('images/<int:pk>/',
         views.ImageDetail.as_view(),
         name='image-details'),
    path('images/<int:pk>/link/<int:life>',
         views.create_expiring_link,
         name='image_link'),
    path('images/<int:pk>/show/',
         views.handle_expiring_link,
         name='display_image'),
]
