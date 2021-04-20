from django.urls import path
from . import views


urlpatterns = [
    path('images/', views.ImageList.as_view()),
    path('images/<int:pk>/', views.ImageDetail.as_view()),
    path('thumbnail200/<int:pk>/', views.thumbnail_200, name='thumbnail200'),
    path('thumbnail400/<int:pk>/', views.thumbnail_400, name='thumbnail400'),
]