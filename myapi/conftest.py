import uuid

import pytest
from django.contrib.auth.models import User
from django.core.files import File
from request_token.models import RequestToken

from api.models import Account, Image


@pytest.fixture
def test_password():
    return r'pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def create_account():
    def make_account(**kwargs):
        user = User.objects.get(username=kwargs['username'])
        if 'username' in kwargs:
            kwargs.pop('username')
        acc = Account(user=user, **kwargs)
        acc.save()
    return make_account


@pytest.fixture
def create_image(create_user, create_account):
    def make_image(**kwargs):
        user = create_user()
        create_account(username=user.username, **kwargs)
        with open('default.JPG', 'rb') as f:
            file = File(f)
            img = Image(image=file, user=user)
            img.save()
            return img
    return make_image


@pytest.fixture
def create_token(create_image):
    def make_token():
        img = create_image()
        token = RequestToken.objects.create_token(
            scope='link',
            data={'img_id': img.id}
        )
        return token
    return make_token
