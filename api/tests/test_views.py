import pytest

from api import views


class TestAliasedUrlViewSet:
    @pytest.mark.parametrize(
        ('mock_get_full_details', 'expected_result'),
        [
            ({}, False),
            (
                    {
                        'url': [1, 2],
                    },
                    False,
            ),
            (
                    {
                        'url': [
                            {
                                'code': 'not_unique',
                            },
                        ],
                    },
                    False,
            ),
            (
                    {
                        'url': [
                            {
                                'code': 'unique',
                            },
                        ],
                    },
                    True,
            ),
        ],
    )
    def test_is_only_unique_url_error(
            self,
            mocker,
            mock_get_full_details,
            expected_result,
    ):
        mocker_error = mocker.Mock(
            get_full_details=mocker.Mock(
                return_value=mock_get_full_details,
            ),
        )
        assert views.AliasedUrlViewSet._is_only_unique_url_error(
            error=mocker_error,
        ) == expected_result
