from typing import Dict
from fastapi.openapi.models import Example

ROOM_EXAMPLES: Dict[str, Example] = {
    "STANDARD_ROOM": {
        "summary": "Стандартный номер",
        "value": {
            "title": "Стандартный номер",
            "description": "Уютный номер с одной двуспальной кроватью, кондиционером и бесплатным Wi-Fi",
            "quantity": 5,
            "price": 3500.00,
            "discount": 10,
            "additionals_ids": []
        }
    },
    "DELUXE_SUITE": {
        "summary": "Люкс Делюкс",
        "value": {
            "title": "Люкс Делюкс",
            "description": "Просторный номер с гостиной зоной, мини-баром и панорамным видом на город",
            "quantity": 5,
            "price": 8500.00,
            "discount": 15,
            "additionals_ids": []
        }
    },
    "FAMILY_ROOM": {
        "summary": "Семейный номер",
        "value": {
            "title": "Семейный номер",
            "description": "Большой номер с двумя кроватями и диваном, идеально подходит для семей с детьми",
            "quantity": 8,
            "price": 5200.00,
            "discount": 12,
            "additionals_ids": []
        }
    },
    "ECONOMY_ROOM": {
        "summary": "Эконом номер",
        "value": {
            "title": "Эконом",
            "description": "Бюджетный вариант с базовыми удобствами для экономных путешественников",
            "quantity": 20,
            "price": 2100.00,
            "discount": 5,
            "additionals_ids": []
        }
    },
    "PRESIDENTIAL_SUITE": {
        "summary": "Президентский люкс",
        "value": {
            "title": "Президентский люкс",
            "description": "Роскошный номер с джакузи, камином и собственной террасой",
            "quantity": 2,
            "price": 15000.00,
            "discount": 20,
            "additionals_ids": []
        }
    },
    "BUSINESS_ROOM": {
        "summary": "Бизнес номер",
        "value": {
            "title": "Бизнес-класс",
            "description": "Номер для деловых путешественников с рабочим столом и конференц-зоной",
            "quantity": 12,
            "price": 5800.00,
            "discount": 14,
            "additionals_ids": []
        }
    },
    "STUDIO_APARTMENT": {
        "summary": "Студия",
        "value": {
            "title": "Студия",
            "description": "Номер-студия с мини-кухней, рабочей зоной и современным дизайном",
            "quantity": 10,
            "price": 4300.00,
            "discount": 8,
            "additionals_ids": []
        }
    },
    "ROMANTIC_ROOM": {
        "summary": "Романтический номер",
        "value": {
            "title": "Романтический номер",
            "description": "Уютный номер для пар с круглой кроватью, шампанским и лепестками роз",
            "quantity": 4,
            "price": 7200.00,
            "discount": 16,
            "additionals_ids": []
        }
    },
    "PENTHOUSE": {
        "summary": "Пентхаус",
        "value": {
            "title": "Пентхаус",
            "description": "Эксклюзивный номер на верхнем этаже с панорамными окнами и собственным лифтом",
            "quantity": 1,
            "price": 18500.00,
            "discount": 25,
            "additionals_ids": []
        }
    },
    "SEA_VIEW_ROOM": {
        "summary": "Номер с видом на море",
        "value": {
            "title": "Номер с видом на море",
            "description": "Прекрасный номер с балконом и захватывающим видом на океан",
            "quantity": 6,
            "price": 8900.00,
            "discount": 18,
            "additionals_ids": []
        }
    }
}
