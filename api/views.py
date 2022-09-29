from django.shortcuts import get_object_or_404, redirect
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from api.models import AliasedUrl
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import AliasedUrlSerializer


class AliasedUrlViewSet(
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = AliasedUrl.objects.all()
    serializer_class = AliasedUrlSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        """Create or return already existing short-url."""
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as error:
            if self._is_only_unique_url_error(error=error):
                return self._return_already_existing_object(url=request.data['url'])
            raise error

    def _return_already_existing_object(self, url: str) -> Response:
        """Returns already existing shortened url."""
        aliased_url = AliasedUrl.objects.get(url=url)
        object_data = {
            'url': aliased_url.url,
            'short_url': aliased_url.short_url,
        }
        headers = self.get_success_headers(object_data)
        return Response(object_data, status=status.HTTP_201_CREATED, headers=headers)

    @staticmethod
    def _is_only_unique_url_error(error: ValidationError) -> bool:
        """Checks if there is only error related to unique url.

        If that happens that means that there is already obj for that url in DB.
        """
        if url_errors := error.get_full_details().get('url'):
            if len(url_errors) == 1:
                # relates to uniques of url field
                return url_errors[0].get('code') == 'unique'
        return False


@api_view()
def resolve_aliased_url(_, alias: str):
    """Resolve shortened URL to proper URL."""
    short_url_obj = get_object_or_404(klass=AliasedUrl, alias=alias)
    return redirect(short_url_obj.url)
