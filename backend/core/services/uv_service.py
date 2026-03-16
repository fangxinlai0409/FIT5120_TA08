from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from math import exp
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

VICTORIA_SA4_CENTERS = [
    ("BARWON", "Barwon", -38.1500, 144.3600),
    ("GIPPSLAND", "Gippsland", -38.1100, 146.4000),
    ("HUME", "Hume", -36.3700, 146.7000),
    ("LODDON_MALLEE", "Loddon Mallee", -36.7500, 144.2800),

    ("MELBOURNE_INNER", "Melbourne Inner", -37.8136, 144.9631),
    ("MELBOURNE_INNER_EAST", "Melbourne Inner East", -37.8100, 145.0800),
    ("MELBOURNE_NORTH_WEST", "Melbourne North West", -37.7000, 144.8500),
    ("MELBOURNE_SOUTH_EAST", "Melbourne South East", -38.0000, 145.2000),
    ("MELBOURNE_WEST", "Melbourne West", -37.8200, 144.7000),
]

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


def get_uv_trend(current_uv: float, hours: int = 10) -> list[dict]:
    mel_tz = ZoneInfo("Australia/Melbourne")
    base = datetime.now(mel_tz)
    trend = []

    peak_hour = 14.5   # 2:30 PM
    peak_uv = 9.0
    end_hour = 18.0    # after 6 PM -> 0

    current_hour = base.hour + base.minute / 60

    def interpolate(x, x0, y0, x1, y1):
        if x <= x0:
            return y0
        if x >= x1:
            return y1
        return y0 + (x - x0) * (y1 - y0) / (x1 - x0)

    for offset in range(hours):
        hour_time = base + timedelta(hours=offset)
        sim_hour = hour_time.hour + hour_time.minute / 60

        if offset == 0:
            uv_value = current_uv

        else:
            # case 1: current time is before 2:30 PM
            if current_hour < peak_hour:
                if sim_hour <= peak_hour:
                    # rise from current real value to peak 9 at 14:30
                    uv_value = interpolate(
                        sim_hour,
                        current_hour, current_uv,
                        peak_hour, peak_uv
                    )
                elif sim_hour <= end_hour:
                    # fall from peak 9 at 14:30 to 0 at 18:00
                    uv_value = interpolate(
                        sim_hour,
                        peak_hour, peak_uv,
                        end_hour, 0.0
                    )
                else:
                    uv_value = 0.0

            # case 2: current time is after 2:30 PM
            else:
                if sim_hour <= end_hour:
                    # continue dropping from current value to 0 by 18:00
                    uv_value = interpolate(
                        sim_hour,
                        current_hour, current_uv,
                        end_hour, 0.0
                    )
                else:
                    uv_value = 0.0

        uv_value = max(0.0, min(9.0, round(uv_value, 1)))
        risk_label, _ = classify_uv(uv_value)

        trend.append({
            "time": hour_time.isoformat(),
            "uv_index": uv_value,
            "risk_level": risk_label,
        })

    return trend


from random import uniform

def get_region_uv_map(current_uv=None):
    results = []

    for code, label, lat, lon in VICTORIA_SA4_CENTERS:
        try:
            uv_index = get_real_uv_value(lat, lon)
        except Exception as e:
            print(f"Failed to fetch UV for {label}: {e}")
            base = current_uv if current_uv is not None else mock_uv_value()
            uv_index = round(max(0, base + uniform(-0.8, 0.8)), 1)

        risk_level, burn_time = classify_uv(uv_index)

        results.append({
            "code": code,
            "label": label,
            "uv_index": uv_index,
            "risk_level": risk_level,
            "burn_time_minutes": burn_time,
        })

    return results
