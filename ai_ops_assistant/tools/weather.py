"""Weather tools using the OpenWeatherMap API."""

from __future__ import annotations

from typing import Any

import requests

from ai_ops_assistant.config import load_settings

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


def current(city: str | None = None, units: str = "metric", **extra_params: Any) -> dict[str, Any]:
    """Fetch current weather for a given city name.

    The planner may call this tool with a ``location`` argument instead of
    ``city``. To be robust we accept arbitrary keyword arguments and fall back
    to ``location`` when ``city`` is not provided.
    """

    if city is None:
        city = str(extra_params.get("location", "")).strip()

    if not city:
        raise ValueError("weather.current requires a city or location name.")

    settings = load_settings()
    if not settings.openweather_api_key:
        raise RuntimeError(
            "OPENWEATHER_API_KEY is not configured; cannot call weather.current."
        )

    params = {"q": city, "appid": settings.openweather_api_key, "units": units}
    resp = requests.get(OPENWEATHER_URL, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    main = data.get("main", {})
    weather_list = data.get("weather", []) or [{}]
    weather = weather_list[0]

    return {
        "city": data.get("name"),
        "country": data.get("sys", {}).get("country"),
        "temperature": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "humidity": main.get("humidity"),
        "description": weather.get("description"),
    }


TOOL_REGISTRY: dict[str, Any] = {
    "weather.current": current,
}

