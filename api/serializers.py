from rest_framework import serializers

from api.models import AliasedUrl


class AliasedUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = AliasedUrl
        fields = (
            'url',
            'short_url',
        )
        read_only_fields = ('short_url',)
