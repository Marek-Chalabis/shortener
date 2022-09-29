from unittest.mock import patch, call

import pytest

from api import const, models
from api.models import AliasedUrl
from shortener import settings


@pytest.mark.django_db
def test_generate_non_taken_alias_for_ul():
    assert len(models._generate_non_taken_alias_for_ul()) == const.START_LENGTH_URL_ALIAS


@pytest.mark.django_db
@patch('api.models.get_random_string')
def test_generate_non_taken_alias_for_ulr_alias_already_exists(mock_get_random_string):
    first_short_url = "ABCDE"
    second_short_url = "ABCDEF"
    # should return second key because first is used
    mock_get_random_string.side_effect = [first_short_url, second_short_url]
    # save object with first key
    AliasedUrl(url='https://www.drf.com', alias=first_short_url).save()
    tested_alias = models._generate_non_taken_alias_for_ul()
    assert tested_alias == second_short_url
    # check if function returns was called again and if alias length expend
    mock_get_random_string.assert_has_calls(
        [
            call(length=const.START_LENGTH_URL_ALIAS),
            call(length=const.START_LENGTH_URL_ALIAS + 1),
        ]
    )


@pytest.mark.django_db
def test_aliased_url_short_url_():
    obj = AliasedUrl(url='https://www.drf.com', alias="ABCDE")
    obj.save()
    assert obj.short_url == f'{settings.DOMAIN}/ABCDE'
