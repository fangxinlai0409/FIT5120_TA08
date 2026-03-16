from datetime import datetime, timedelta, timezone
from random import uniform
import requests
from django.conf import settings
from core.models import Location, ProtectionRule, UVReading

UV_BUCKETS = [
    (0, 2.9, "Low", 45),
    (3, 5.9, "Moderate", 30),
    (6, 7.9, "High", 20),
    (8, 10.9, "Very High", 12),
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

LOCATION_COORDS = {
    "Melbourne": (-37.8136, 144.9631),
    "Geelong": (-38.1499, 144.3617),
    "Bendigo": (-36.7570, 144.2794),
}

def classify_uv(uv_value: float) -> tuple[str, int]:
    if uv_value < 3:
        return "Low", 45
    elif uv_value < 6:
        return "Moderate", 30
    elif uv_value < 8:
        return "High", 20
    elif uv_value < 11:
        return "Very High", 12
    else:
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
    return round(uniform(0, 2.5), 1)

def get_real_uv_value(latitude: float, longitude: float) -> float:
    api_key = settings.OPENWEATHER_API_KEY
    if not api_key:
        raise ValueError("open weather api key missing")
    
    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": latitude,
        "lon": longitude,
        "exclude": "minutely,hourly,daily,alerts",
        "appid": api_key,
    }

    response = requests.get(url, params=params, timeout=8)
    response.raise_for_status()

    data = response.json()
    uvi = data.get("current",{}).get("uvi")

    if uvi is None:
        raise ValueError("UV index not found in open weather response")

    return round(float(uvi),1)

def get_current_uv(location_name: str | None = None, lat: str | None = None, lon: str | None = None) -> UVReading:
    if lat is not None and lon is not None:
        latitude = float(lat)
        longitude = float(lon)

        location = Location.objects.filter(name="Your location").first()
        if not location:
            location = Location.objects.create(
                name="Your location",
                latitude=latitude,
                longitude=longitude,
            )
        else:
            location.latitude = latitude
            location.longitude = longitude
            location.save()

    else:
        if location_name is None:
            location_name = "Melbourne"

        location = Location.objects.filter(name=location_name).first()
        if not location:
            location = Location.objects.get(name="Melbourne")

        latitude = location.latitude
        longitude = location.longitude

    try:
        uv_value = get_real_uv_value(latitude, longitude)
    except Exception as e:
        print(f"OpenWeather UV fetch failed: {e}")
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


def get_uv_trend(current_uv: float, hours: int = 6) -> list[dict]:
    base = datetime.now(timezone.utc)
    trend = []

    for offset in range(hours):
        hour_time = base + timedelta(hours=offset)

        if offset == 0:
            uv_value = current_uv
        else:
            uv_value = current_uv + (3 - offset) * uniform(0.3, 0.8)

        risk_label, _ = classify_uv(uv_value)

        trend.append({
            "time": hour_time.isoformat(),
            "uv_index": round(uv_value, 1),
            "risk_level": risk_label,
        })

    return trend


def get_region_uv_map(current_uv: float | None = None) -> list[dict]:
    snapshot = []
    for code, baseline in REGIONAL_BASELINES.items():
        if code == "VIC" and current_uv is not None:
            uv_value = round(float(current_uv), 1)
        else:
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
