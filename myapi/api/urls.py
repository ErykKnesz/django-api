from django.urls import path
from . import views


urlpatterns = [
    path('images/', views.ImageList.as_view()),
    path('images/<int:pk>/', views.ImageDetail.as_view()),
    path('thumbnail', views.thumbnail_200, name='thumbnail200')
]