from typing import Dict
from fastapi.openapi.models import Example

BOOKING_EXAMPLES: Dict[str, Example] = {
    "WEEKEND_BOOKING": {
        "summary": "Бронирование на выходные",
        "value": {
            "room_id": 1,
            "date_from": "2025-07-05",
            "date_to": "2025-07-07"
        }
    },
    "BUSINESS_TRIP": {
        "summary": "Командировка на неделю",
        "value": {
            "room_id": 6,
            "date_from": "2025-08-15",
            "date_to": "2025-08-22"
        }
    },
    "FAMILY_VACATION": {
        "summary": "Семейный отпуск",
        "value": {
            "room_id": 3,
            "date_from": "2025-09-10",
            "date_to": "2025-09-17"
        }
    },
    "ROMANTIC_GETAWAY": {
        "summary": "Романтический уикенд",
        "value": {
            "room_id": 8,
            "date_from": "2025-07-25",
            "date_to": "2025-07-28"
        }
    },
    "LUXURY_STAY": {
        "summary": "Роскошное проживание",
        "value": {
            "room_id": 5,
            "date_from": "2025-10-01",
            "date_to": "2025-10-05"
        }
    },
    "EXTENDED_STAY": {
        "summary": "Длительное проживание",
        "value": {
            "room_id": 7,
            "date_from": "2025-11-15",
            "date_to": "2025-11-30"
        }
    },
    "CONFERENCE_BOOKING": {
        "summary": "Бронирование на конференцию",
        "value": {
            "room_id": 6,
            "date_from": "2025-09-20",
            "date_to": "2025-09-23"
        }
    },
    "HOLIDAY_BOOKING": {
        "summary": "Новогодние праздники",
        "value": {
            "room_id": 2,
            "date_from": "2025-12-30",
            "date_to": "2026-01-03"
        }
    },
    "SUMMER_VACATION": {
        "summary": "Летний отпуск",
        "value": {
            "room_id": 10,
            "date_from": "2025-08-01",
            "date_to": "2025-08-14"
        }
    },
    "SHORT_STAY": {
        "summary": "Краткосрочное проживание",
        "value": {
            "room_id": 4,
            "date_from": "2025-07-18",
            "date_to": "2025-07-20"
        }
    }
}
