# from django.test import TestCase
from django.contrib.auth.models import User
import pytest
from django.urls import reverse


def test_view_image_list_without_credentials(client):
    url = reverse('image_list')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_view_image_list_with_credentials(client, create_user,
                                          test_password,
                                          create_account):
    user = create_user(username='someone')
    create_account(username=user.username)
    client.login(username=user.username, password=test_password)
    url = reverse('image_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_image_list_shows_images(client, create_image, test_password):
    img = create_image(type='Premium')
    user = User.objects.latest('id')

    client.login(username=user.username, password=test_password)
    url = reverse('image_list')
    response = client.get(url)

    if user.account.is_base():
        img_name = img.image.name
        img_name = img_name[:-4]
        assert img_name in response.data[0]['small_thumbnail']
    else:
        assert img.image.name in response.data[0]['image']


