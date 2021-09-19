import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import FileResponse

from .models import Image


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
def test_view_image_list_shows_images_for_base(client, create_image,
                                               test_password):
    img = create_image()
    user = User.objects.latest('id')
    client.login(username=user.username, password=test_password)
    url = reverse('image_list')
    response = client.get(url)

    img_name = img.image.name
    img_name = img_name[:-4]

    assert img_name in response.data[0]['small_thumbnail']


@pytest.mark.django_db
def test_view_image_list_shows_images_for_premium(client, create_image,
                                                  test_password):
    img = create_image(type='Premium')
    user = User.objects.latest('id')
    client.login(username=user.username, password=test_password)
    url = reverse('image_list')
    response = client.get(url)
    assert img.image.name in response.data[0]['image']
    assert img.small_thumbnail.name in response.data[0]['small_thumbnail']
    assert img.big_thumbnail.name in response.data[0]['big_thumbnail']


@pytest.mark.django_db
def test_view_image_list_shows_images_for_enterprise(client, create_image,
                                                     test_password):
    img = create_image(type='Enterprise')
    user = User.objects.latest('id')
    client.login(username=user.username, password=test_password)
    url = reverse('image_list')
    response = client.get(url)
    assert img.image.name in response.data[0]['image']
    assert img.small_thumbnail.name in response.data[0]['small_thumbnail']
    assert img.big_thumbnail.name in response.data[0]['big_thumbnail']


@pytest.mark.django_db
def test_view_image_detail_shows_images_for_base(client, create_image,
                                                 test_password):
    img = create_image()
    user = User.objects.latest('id')
    client.login(username=user.username, password=test_password)
    url = reverse('image-details', args=[user.id])
    response = client.get(url)

    img_name = img.image.name
    img_name = img_name[:-4]

    assert img_name in response.data['small_thumbnail']


@pytest.mark.django_db
def test_view_image_detail_shows_images_for_premium(client, create_image,
                                                    test_password):
    img = create_image(type='Premium')
    user = User.objects.latest('id')
    client.login(username=user.username, password=test_password)
    url = reverse('image-details', args=[user.id])
    response = client.get(url)
    assert img.image.name in response.data['image']
    assert img.small_thumbnail.name in response.data['small_thumbnail']
    assert img.big_thumbnail.name in response.data['big_thumbnail']


@pytest.mark.django_db
def test_view_image_detail_shows_images_for_enterprise(client, create_image,
                                                       test_password):
    img = create_image(type='Enterprise')
    user = User.objects.latest('id')
    client.login(username=user.username, password=test_password)
    url = reverse('image-details', args=[user.id])
    response = client.get(url)
    assert img.image.name in response.data['image']
    assert img.small_thumbnail.name in response.data['small_thumbnail']
    assert img.big_thumbnail.name in response.data['big_thumbnail']


@pytest.mark.django_db
def test_view_create_image_with_get_method(client, create_user, create_account,
                                           test_password):
    user = create_user(username='someone')
    create_account(username=user.username)
    client.login(username=user.username, password=test_password)
    url = reverse('create_image')
    response = client.get(url)
    assert response.status_code == 405


def test_view_create_image_without_credentials(client):
    url = reverse('create_image')
    response = client.post(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_view_create_image_posts_image(client, create_user, create_account,
                                       test_password):
    user = create_user(username='someone')
    create_account(username=user.username)
    client.login(username=user.username, password=test_password)
    url = reverse('create_image')
    with open('default.JPG', 'rb') as f:
        response = client.post(url, {'image': f, 'user': user})
    img = Image.objects.latest('id')
    img_name = img.image.name
    img_name = img_name[:-4]

    assert response.status_code == 201
    assert 'default' in img_name


@pytest.mark.django_db
def test_view_create_image_creates_thmb_for_base(client, create_user,
                                                 create_account,
                                                 test_password):
    user = create_user(username='someone')
    create_account(username=user.username)
    client.login(username=user.username, password=test_password)
    url = reverse('create_image')
    with open('default.JPG', 'rb') as f:
        client.post(url, {'image': f, 'user': user})
    img = Image.objects.latest('id')
    assert not img.big_thumbnail
    assert img.small_thumbnail


@pytest.mark.django_db
def test_view_create_image_creates_thmb_for_non_base(client, create_user,
                                                     create_account,
                                                     test_password):
    user = create_user(username='someone')
    create_account(username=user.username, type='E')
    client.login(username=user.username, password=test_password)
    url = reverse('create_image')
    with open('default.JPG', 'rb') as f:
        client.post(url, {'image': f, 'user': user})
    img = Image.objects.latest('id')

    assert img.big_thumbnail
    assert img.small_thumbnail


@pytest.mark.django_db
def test_view_create_expiring_link_30000_sec(client, create_image,
                                             test_password):
    create_image(type='E')
    user = User.objects.latest('id')
    client.login(username=user.username, password=test_password)
    url = reverse('image_link', args=[1, 30000])
    response = client.get(url)
    assert response.status_code == 200
    assert 'expiring link' in response.data
    assert (response.data['claims']['exp']
            - response.data['claims']['iat']
            == 30000
            )


@pytest.mark.django_db
def test_view_create_expiring_link_30001_sec(client, create_image,
                                             test_password):
    create_image(type='E')
    user = User.objects.latest('id')
    client.login(username=user.username, password=test_password)
    url = reverse('image_link', args=[1, 30001])
    response = client.get(url)
    assert response.status_code == 400


@pytest.mark.django_db
def test_view_create_expiring_link_29_sec(client, create_image,
                                          test_password):
    create_image(type='E')
    user = User.objects.latest('id')
    client.login(username=user.username, password=test_password)
    url = reverse('image_link', args=[1, 29])
    response = client.get(url)
    assert response.status_code == 400


@pytest.mark.django_db
def test_access_create_expiring_link_no_img_owner(client, create_image,
                                                  test_password):
    create_image(type='E')
    create_image()
    user = User.objects.get(pk=2)
    client.login(username=user.username, password=test_password)
    url = reverse('image_link', args=[1, 30])
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_access_create_expiring_link_no_enterprise(client, create_image,
                                                   test_password):
    create_image(type='P')
    user = User.objects.get(pk=1)
    client.login(username=user.username, password=test_password)
    url = reverse('image_link', args=[1, 30])
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_view_handle_expiring_link_no_token(client, create_image):
    create_image()
    url = reverse('display_image')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_view_handle_expiring_link_with_token(client, create_image,
                                              create_token):
    create_image()
    token = create_token()
    url = reverse('display_image') + "?rt=" + token.jwt()
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response, FileResponse)