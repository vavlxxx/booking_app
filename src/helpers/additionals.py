from typing import Dict
from fastapi.openapi.models import Example

ADDITIONALS_EXAMPLES: Dict[str, Example] = {
    "AIR_CONDITIONING": {
        "summary": "Кондиционер",
        "value": {
            "name": "Кондиционер",
            "description": "Индивидуальный климат-контроль с возможностью регулировки температуры",
        },
    },
    "FREE_WIFI": {
        "summary": "Бесплатный Wi-Fi",
        "value": {
            "name": "Бесплатный Wi-Fi",
            "description": "Высокоскоростной беспроводной интернет во всех номерах",
        },
    },
    "MINIBAR": {
        "summary": "Мини-бар",
        "value": {"name": "Мини-бар", "description": "Холодильник с напитками и закусками"},
    },
    "SAFE_BOX": {
        "summary": "Сейф",
        "value": {"name": "Сейф", "description": "Электронный сейф для хранения ценностей"},
    },
    "FLAT_SCREEN_TV": {
        "summary": "Телевизор",
        "value": {
            "name": "LED телевизор",
            "description": "Плоский экран с кабельными и спутниковыми каналами",
        },
    },
    "ROOM_SERVICE": {
        "summary": "Обслуживание номеров",
        "value": {
            "name": "Room Service 24/7",
            "description": "Круглосуточное обслуживание номеров с доставкой еды и напитков",
        },
    },
    "BALCONY": {
        "summary": "Балкон",
        "value": {
            "name": "Балкон с видом",
            "description": "Частный балкон с мебелью и красивым видом",
        },
    },
    "JACUZZI": {
        "summary": "Джакузи",
        "value": {"name": "Джакузи", "description": "Гидромассажная ванна для релаксации"},
    },
    "WORK_DESK": {
        "summary": "Рабочий стол",
        "value": {
            "name": "Рабочая зона",
            "description": "Удобный письменный стол с эргономичным креслом и хорошим освещением",
        },
    },
    "KITCHENETTE": {
        "summary": "Мини-кухня",
        "value": {
            "name": "Мини-кухня",
            "description": "Компактная кухня с микроволновой печью, холодильником и посудой",
        },
    },
    "IRON_BOARD": {
        "summary": "Утюг и гладильная доска",
        "value": {
            "name": "Утюг и гладильная доска",
            "description": "Утюг с гладильной доской для ухода за одеждой",
        },
    },
    "COFFEE_MACHINE": {
        "summary": "Кофемашина",
        "value": {
            "name": "Кофемашина",
            "description": "Капсульная кофемашина с набором капсул и чаем",
        },
    },
    "BATHROBE_SLIPPERS": {
        "summary": "Халаты и тапочки",
        "value": {
            "name": "Халаты и тапочки",
            "description": "Мягкие махровые халаты и одноразовые тапочки",
        },
    },
    "SOUNDPROOFING": {
        "summary": "Шумоизоляция",
        "value": {
            "name": "Звукоизоляция",
            "description": "Качественная шумоизоляция для комфортного отдыха",
        },
    },
    "PREMIUM_TOILETRIES": {
        "summary": "Премиум косметика",
        "value": {
            "name": "Премиум туалетные принадлежности",
            "description": "Косметические средства известных брендов: шампунь, гель, лосьон",
        },
    },
}
