from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import resolve_aliased_url, AliasedUrlViewSet

router_v1 = DefaultRouter()
router_v1.register('aliased-url', AliasedUrlViewSet, basename='aliased-url')

urlpatterns = [
    path('<str:alias>', resolve_aliased_url),
    path('api/v1/', include(router_v1.urls)),
]
