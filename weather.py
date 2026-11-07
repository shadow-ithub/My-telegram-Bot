from datetime import datetime

import requests

API_URL = "https://api.open-meteo.com/v1/forecast"

LOCATION = {
    "name": "Нальчик",
    "latitude": 43.4981,
    "longitude": 43.6189,
    "timezone": "Europe/Moscow",
}

WEEKDAYS = [
    "понедельник",
    "вторник",
    "среда",
    "четверг",
    "пятница",
    "суббота",
    "воскресенье",
]

MONTHS = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
]

WEATHER_CODES = {
    0: "Ясно",
    1: "Преимущественно ясно",
    2: "Переменная облачность",
    3: "Пасмурно",
    45: "Туман",
    48: "Изморозь",
    51: "Слабая морось",
    53: "Морось",
    55: "Сильная морось",
    56: "Ледяная морось",
    57: "Сильная ледяная морось",
    61: "Слабый дождь",
    63: "Дождь",
    65: "Сильный дождь",
    66: "Ледяной дождь",
    67: "Сильный ледяной дождь",
    71: "Слабый снег",
    73: "Снег",
    75: "Сильный снег",
    77: "Снежная крупа",
    80: "Слабый ливень",
    81: "Ливень",
    82: "Сильный ливень",
    85: "Слабый снегопад",
    86: "Сильный снегопад",
    95: "Гроза",
    96: "Гроза с мелким градом",
    99: "Гроза с крупным градом",
}

_MD_SPECIAL = set(r"_*[]()~`>#+-=|{}.!\\")


def _esc(value):
    return "".join("\\" + char if char in _MD_SPECIAL else char for char in str(value))


def _code(value):
    text = str(value)
    return text.replace("\\", "\\\\").replace("`", "\\`")


def _fetch_daily():
    response = requests.get(
        API_URL,
        params={
            "latitude": LOCATION["latitude"],
            "longitude": LOCATION["longitude"],
            "daily": ",".join(
                [
                    "weather_code",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_probability_max",
                    "wind_speed_10m_max",
                ]
            ),
            "timezone": LOCATION["timezone"],
            "forecast_days": 7,
            "wind_speed_unit": "ms",
        },
        timeout=15,
    )
    response.raise_for_status()
    return response.json()["daily"]


def build_forecast_markdown():
    daily = _fetch_daily()

    lines = [
        "*Погода — Кабардино\\-Балкария*",
        f"_{_esc(LOCATION['name'])} · 7 дней_",
        "",
    ]

    for index, date_string in enumerate(daily["time"]):
        date = datetime.strptime(date_string, "%Y-%m-%d")
        day_name = WEEKDAYS[date.weekday()].capitalize()
        month = MONTHS[date.month - 1]

        t_max = daily["temperature_2m_max"][index]
        t_min = daily["temperature_2m_min"][index]
        precipitation = daily["precipitation_probability_max"][index]
        wind = daily["wind_speed_10m_max"][index]
        description = WEATHER_CODES.get(daily["weather_code"][index], "Нет данных")

        t_max_text = "—" if t_max is None else f"{t_max:+.0f}°".replace("-", "−")
        t_min_text = "—" if t_min is None else f"{t_min:+.0f}°".replace("-", "−")
        precipitation_text = "—" if precipitation is None else f"{precipitation}%"
        wind_text = "—" if wind is None else f"{wind:.1f} м/с"

        lines.append(f"*{_esc(day_name)}, {_esc(date.day)} {_esc(month)}*")
        lines.append(
            f"Максимум `{_code(t_max_text)}` · минимум `{_code(t_min_text)}`"
        )
        lines.append(f"_{_esc(description)}_")
        lines.append(
            f"Осадки `{_code(precipitation_text)}` · ветер `{_code(wind_text)}`"
        )
        lines.append("")

    lines.append(f"[{_esc('Open-Meteo')}](https://open-meteo.com)")

    return "\n".join(lines)
