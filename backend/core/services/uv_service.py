from datetime import datetime, timedelta, timezone
from random import uniform

from core.models import Location, ProtectionRule, UVReading

UV_BUCKETS = [
    (0, 2, "Low", 45),
    (3, 5, "Moderate", 30),
    (6, 7, "High", 20),
    (8, 10, "Very High", 12),
    (11, 15, "Extreme", 8),
]

REGIONAL_BASELINES = {
    "WA": 9.2,
    "NT": 10.1,
    "SA": 7.4,
    "QLD": 10.5,
    "NSW": 8.6,
    "ACT": 8.2,
    "VIC": 7.1,
    "TAS": 5.9,
}

REGION_LABELS = {
    "WA": "Western Australia",
    "NT": "Northern Territory",
    "SA": "South Australia",
    "QLD": "Queensland",
    "NSW": "New South Wales",
    "ACT": "Australian Capital Territory",
    "VIC": "Victoria",
    "TAS": "Tasmania",
}


def classify_uv(uv_value: float) -> tuple[str, int]:
    for min_uv, max_uv, label, burn_minutes in UV_BUCKETS:
        if min_uv <= uv_value <= max_uv:
            return label, burn_minutes
    return "Extreme", 8


def get_or_create_default_location() -> Location:
    location, _ = Location.objects.get_or_create(
        name="Melbourne CBD",
        defaults={
            "city": "Melbourne",
            "state": "Victoria",
            "latitude": -37.8136,
            "longitude": 144.9631,
        },
    )
    return location


def mock_uv_value() -> float:
    # Simple deterministic mock based on current hour window.
    current_hour = datetime.now().hour
    if 6 <= current_hour <= 18:
        return round(uniform(3.5, 11.0), 1)
    return round(uniform(0.0, 2.5), 1)


def get_current_uv(location_name: str | None = None) -> UVReading:
    location = get_or_create_default_location()
    uv_value = mock_uv_value()
    risk_label, burn_minutes = classify_uv(uv_value)
    reading = UVReading.objects.create(
        location=location,
        uv_index=uv_value,
        risk_level=risk_label,
        burn_time_minutes=burn_minutes,
        observation_time=datetime.now(timezone.utc),
    )
    return reading


def get_protection_advice(uv_value: float) -> str:
    rule = (
        ProtectionRule.objects.filter(min_uv__lte=uv_value, max_uv__gte=uv_value)
        .order_by("min_uv")
        .first()
    )
    if rule:
        return rule.recommendation
    # Fallback if the DB isn't populated yet.
    _, burn_minutes = classify_uv(uv_value)
    return f"UV {uv_value}: apply broad-spectrum SPF50+, seek shade within {burn_minutes} minutes."


def get_uv_trend(hours: int = 6) -> list[dict]:
    base = datetime.now(timezone.utc)
    trend = []
    for offset in range(hours):
        hour_time = base + timedelta(hours=offset)
        uv_value = max(0, mock_uv_value() - offset * 0.5)
        risk_label, _ = classify_uv(uv_value)
        trend.append({
            "time": hour_time.isoformat(),
            "uv_index": uv_value,
            "risk_level": risk_label,
        })
    return trend


def get_region_uv_map() -> list[dict]:
    snapshot = []
    for code, baseline in REGIONAL_BASELINES.items():
        uv_value = round(max(0, baseline + uniform(-1.5, 1.5)), 1)
        risk_label, burn_minutes = classify_uv(uv_value)
        snapshot.append(
            {
                "code": code,
                "label": REGION_LABELS[code],
                "uv_index": uv_value,
                "risk_level": risk_label,
                "burn_time_minutes": burn_minutes,
            }
        )
    return snapshot
