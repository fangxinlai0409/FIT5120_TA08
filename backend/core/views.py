from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CancerStatistic, ProtectionRule
from .serializers import (
    CancerStatisticSerializer,
    ProtectionRuleSerializer,
    UVReadingSerializer,
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
        location = request.query_params.get("location")
        reading = get_current_uv(location)
        serializer = UVReadingSerializer(reading)
        warning = build_warning(reading.uv_index, reading.risk_level, reading.burn_time_minutes)
        return Response(
            {
                "reading": serializer.data,
                "warning": warning,
                "trend": get_uv_trend(),
                "fetched_at": datetime.utcnow().isoformat() + "Z",
            }
        )


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
        stats = CancerStatistic.objects.all()
        return Response({"data": CancerStatisticSerializer(stats, many=True).data})


class UVRegionView(APIView):
    def get(self, request):
        return Response({"regions": get_region_uv_map()})


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
    suffix = f"Your skin may burn in about {burn_minutes} minutes." if burn_minutes else "Protect your skin."
    additions = {
        "Low": "Protection optional unless outside for extended periods.",
        "Moderate": "Slip on a shirt and apply SPF30+ sunscreen.",
        "High": "Add a wide-brim hat and sunglasses.",
        "Very High": "Seek shade during peak hours (10am-3pm).",
        "Extreme": "Minimise time outdoors, cover up fully.",
    }
    advice = additions.get(risk_label, "Use multiple sun protection measures.")
    return f"UV {uv_value} ({risk_label}). {suffix} {advice}"
