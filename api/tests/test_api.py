import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from api import models

TEST_URL = 'https://www.drf.com/tylkojednowglowiemam'


class TestAliasedUrlViewSet(APITestCase):
    @pytest.mark.django_db
    def test_create(self):
        response = self.client.post(
            path='/api/v1/aliased-url/',
            data={
                'url': TEST_URL,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        # check if object exists and is properly saved
        saved_obj = models.AliasedUrl.objects.all()[0]
        assert saved_obj.url == TEST_URL
        assert response.json()['short_url'].endswith(saved_obj.alias)
        assert models.AliasedUrl.objects.all()[0].url

    @pytest.mark.django_db
    def test_create_obj_exists(self):
        aliased_url = models.AliasedUrl(url=TEST_URL, alias="OMG")
        aliased_url.save()
        response = self.client.post(
            path='/api/v1/aliased-url/',
            data={
                'url': aliased_url.url,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['url'] == aliased_url.url
        # there is only one object second was not created
        assert models.AliasedUrl.objects.count() == 1


class TestResolveAliasedUrl(APITestCase):

    @pytest.mark.django_db
    def test_resolve_aliased_url_obj_exists(self):
        aliased_url = models.AliasedUrl(url=TEST_URL, alias="OMG")
        aliased_url.save()
        response = self.client.get(
            path=f'/{aliased_url.alias}',
        )
        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == aliased_url.url

    def test_resolve_aliased_url_obj_not_exists(self):
        response = self.client.get(
            path='/sad_frog',
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
