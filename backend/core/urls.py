from django.urls import path

from .views import (
    CancerStatisticView,
    CurrentUVView,
    ProtectionAdviceView,
    UVMessageView,
    UVRegionView,
)

urlpatterns = [
    path("uv/current/", CurrentUVView.as_view(), name="uv-current"),
    path("uv/message/", UVMessageView.as_view(), name="uv-message"),
    path("uv/regions/", UVRegionView.as_view(), name="uv-regions"),
    path("cancer-stats/", CancerStatisticView.as_view(), name="cancer-stats"),
    path("protection/", ProtectionAdviceView.as_view(), name="protection-advice"),
]
