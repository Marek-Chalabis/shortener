from django.db import models
from django.utils.crypto import get_random_string

from api import const
import itertools

from shortener import settings


def _generate_non_taken_alias_for_ul() -> str:
    """Creates unique alias for AliasedUrl object.

    If alias is already in DB make new one with one character longer.
    """
    for i in itertools.count():
        alias = get_random_string(length=const.START_LENGTH_URL_ALIAS + i)
        if AliasedUrl.objects.filter(alias=alias).exists():
            continue
        return alias


class AliasedUrl(models.Model):
    """URL with shortened alias."""
    url = models.URLField(max_length=300, unique=True, help_text="Main URL")
    alias = models.URLField(
        unique=True,
        help_text="URL alias for full url path",
        default=_generate_non_taken_alias_for_ul,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def short_url(self) -> str:
        """Url with current domain and alias."""
        return f'{settings.DOMAIN}/{self.alias}'
