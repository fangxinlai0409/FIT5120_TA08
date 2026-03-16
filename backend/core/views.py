from datetime import datetime, timezone

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CancerStatistic, ProtectionRule, MelanomaMortalityStatistic
from .serializers import (
    CancerStatisticSerializer,
    ProtectionRuleSerializer,
    UVReadingSerializer,
    MelanomaMortalityStatisticSerializer,
)
from .services.uv_service import (
    classify_uv,
    get_current_uv,
    get_protection_advice,
    get_region_uv_map,
    get_uv_trend,
)


class CurrentUVView(APIView):
    def get(self, request):
        location = request.query_params.get("location", "Melbourne")
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")

        reading = get_current_uv(location_name=location, lat=lat, lon=lon)
        serializer = UVReadingSerializer(reading)

        trend = get_uv_trend(reading.uv_index)

        return Response({
            "reading": serializer.data,
            "trend": trend,
            "fetched_at": datetime.now(timezone.utc),
        })


class UVMessageView(APIView):
    def get(self, request):
        uv_value = float(request.query_params.get("uv", 0))
        risk_label, burn_minutes = classify_uv(uv_value)
        return Response(
            {
                "uv_index": uv_value,
                "risk_level": risk_label,
                "warning": build_warning(uv_value, risk_label, burn_minutes),
            }
        )


class CancerStatisticView(APIView):
    def get(self, request):
        sex = request.query_params.get("sex", "Persons")
        stats = CancerStatistic.objects.filter(sex=sex).order_by("year")
        return Response({"data": CancerStatisticSerializer(stats, many=True).data})

class UVRegionView(APIView):
    def get(self, request):
        current_uv = request.GET.get("uv")

        if current_uv is not None:
            current_uv = float(current_uv)

        return Response({
            "regions": get_region_uv_map(current_uv=current_uv)
        })


class ProtectionAdviceView(APIView):
    def get(self, request):
        uv_value = request.query_params.get("uv")
        rules = ProtectionRule.objects.all()
        serializer = ProtectionRuleSerializer(rules, many=True)
        highlighted = None
        if uv_value is not None:
            uv_val = float(uv_value)
            highlighted = get_protection_advice(uv_val)
        return Response({
            "rules": serializer.data,
            "recommended": highlighted,
        })


def build_warning(uv_value: float, risk_label: str, burn_minutes: int | None) -> str:
    suffix = f"Unprotected skin will burn within {burn_minutes} minutes." if burn_minutes else "Protect your skin."
    additions = {
        "Low": "Use SPF 30+ sunscreen when outside for extended periods.",
        "Moderate": "Wear sunglasses and reapply sunscreen every two hours.",
        "High": "Add a wide-brim hat and sunglasses. Reapply SPF 50+ sunscreen immediately after swimming.",
        "Very High": "Seek shade during peak hours (10am-3pm). Wear UV protective clothing.",
        "Extreme": "Avoid direct contact with sunlight, cover up fully.",
    }
    advice = additions.get(risk_label, "Use multiple sun protection measures.")
    return f"UV {uv_value} ({risk_label}). {suffix} {advice}"

class MelanomaMortalityStatisticView(APIView):
    def get(self, request):
        sex = request.query_params.get("sex", "Persons")
        age_group = request.query_params.get("age_group", "15-24")

        stats = MelanomaMortalityStatistic.objects.filter(
            sex=sex,
            age_group=age_group,
        ).order_by("year")

        return Response({
            "data": MelanomaMortalityStatisticSerializer(stats, many=True).data
        })