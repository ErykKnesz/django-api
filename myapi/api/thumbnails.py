from django.conf import settings
import os

def create_thumbnail(instance, size):
    img = instance.open_image()
    path = instance.image.path
    name = instance.image.name
    name_suffix = f'thumbnail{size}'
    if path.lower().endswith('.jpg') or path.lower().endswith('.png'):
        path = path[:-4]
        ext = name[-4:]
        name = name[:-4]
    if path.lower().endswith('.jpeg'):
        path = path[:-5]
        ext = name[-5:]
        name = name[:-5]
    name = name + name_suffix + ext
    path += name_suffix + ext
    small_size = (200, img.width)
    img.thumbnail(small_size)
    img.save(path)
    return name


def create_thumbnail_200(instance):
    thumbnail_name = create_thumbnail(instance, 200)
    return thumbnail_name


def create_thumbnail_400(instance):
    thumbnail_name = create_thumbnail(instance, 400)
    return thumbnail_name