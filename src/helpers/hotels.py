from typing import Dict
from fastapi.openapi.models import Example

HOTEL_EXAMPLES: Dict[str, Example] = {
    "RITZ": {
        "summary": "PARIS RITZ",
        "value": {
            "location": "Париж",
            "title": "RITZ",
            "description": "Легендарный отель в самом сердце Парижа, символ роскоши и французского шика",
        },
    },
    "IMPERIAL": {
        "summary": "TOKYO IMPERIAL",
        "value": {
            "location": "Токио",
            "title": "IMPERIAL",
            "description": "Престижный отель в центре Токио с традиционным японским сервисом",
        },
    },
    "SAVOY": {
        "summary": "LONDON SAVOY",
        "value": {
            "location": "Лондон",
            "title": "SAVOY",
            "description": "Исторический отель в театральном районе Лондона с викторианской элегантностью",
        },
    },
    "BURJ AL ARAB": {
        "summary": "DUBAI BURJ AL ARAB",
        "value": {
            "location": "Дубай",
            "title": "BURJ AL ARAB",
            "description": "Знаменитый парусообразный отель-символ Дубая с непревзойденной роскошью",
        },
    },
    "PLAZA": {
        "summary": "NEW YORK PLAZA",
        "value": {
            "location": "Нью-Йорк",
            "title": "PLAZA",
            "description": "Культовый отель на Пятой авеню напротив Центрального парка",
        },
    },
    "EXCELSIOR": {
        "summary": "ROME EXCELSIOR",
        "value": {
            "location": "Рим",
            "title": "EXCELSIOR",
            "description": "Элегантный отель рядом с виллой Боргезе в самом центре Вечного города",
        },
    },
    "MAJESTIC": {
        "summary": "BARCELONA MAJESTIC",
        "value": {
            "location": "Барселона",
            "title": "MAJESTIC",
            "description": "Роскошный отель на Пасео де Грасия в сердце каталонской столицы",
        },
    },
    "RAFFLES": {
        "summary": "SINGAPORE RAFFLES",
        "value": {
            "location": "Сингапур",
            "title": "RAFFLES",
            "description": "Колониальный отель-легенда, родина коктейля Singapore Sling",
        },
    },
    "FOUR SEASONS": {
        "summary": "ISTANBUL FOUR SEASONS",
        "value": {
            "location": "Стамбул",
            "title": "FOUR SEASONS",
            "description": "Современный отель с видом на Босфор в историческом районе Султанахмет",
        },
    },
    "WESTIN PALACE": {
        "summary": "MADRID WESTIN PALACE",
        "value": {
            "location": "Мадрид",
            "title": "WESTIN PALACE",
            "description": "Величественный отель в центре Мадрида с королевской атмосферой",
        },
    },
    "WALDORF ASTORIA": {
        "summary": "AMSTERDAM WALDORF ASTORIA",
        "value": {
            "location": "Амстердам",
            "title": "WALDORF ASTORIA",
            "description": "Роскошный отель в историческом здании на знаменитых каналах",
        },
    },
    "GOLDEN WELL": {
        "summary": "PRAGUE GOLDEN WELL",
        "value": {
            "location": "Прага",
            "title": "GOLDEN WELL",
            "description": "Бутик-отель в барочном дворце с видом на Пражский град",
        },
    },
    "SACHER": {
        "summary": "VIENNA SACHER",
        "value": {
            "location": "Вена",
            "title": "SACHER",
            "description": "Легендарный отель напротив Венской оперы, родина торта Захер",
        },
    },
    "BULGARI": {
        "summary": "MILAN BULGARI",
        "value": {
            "location": "Милан",
            "title": "BULGARI",
            "description": "Стильный отель от знаменитого ювелирного дома в квадрате моды",
        },
    },
    "BAYERISCHER HOF": {
        "summary": "MUNICH BAYERISCHER HOF",
        "value": {
            "location": "Мюнхен",
            "title": "BAYERISCHER HOF",
            "description": "Традиционный баварский отель в центре города с богатой историей",
        },
    },
    "BAUR AU LAC": {
        "summary": "ZURICH BAUR AU LAC",
        "value": {
            "location": "Цюрих",
            "title": "BAUR AU LAC",
            "description": "Элитный отель на берегу Цюрихского озера с альпийским шармом",
        },
    },
    "D'ANGLETERRE": {
        "summary": "COPENHAGEN D'ANGLETERRE",
        "value": {
            "location": "Копенгаген",
            "title": "D'ANGLETERRE",
            "description": "Исторический отель на главной площади датской столицы",
        },
    },
    "GRAND HOTEL": {
        "summary": "STOCKHOLM GRAND HOTEL",
        "value": {
            "location": "Стокгольм",
            "title": "GRAND HOTEL",
            "description": "Знаменитый отель на набережной с видом на Королевский дворец",
        },
    },
    "CONTINENTAL": {
        "summary": "OSLO CONTINENTAL",
        "value": {
            "location": "Осло",
            "title": "CONTINENTAL",
            "description": "Престижный отель в самом центре норвежской столицы",
        },
    },
    "KÄMP": {
        "summary": "HELSINKI KÄMP",
        "value": {
            "location": "Хельсинки",
            "title": "KÄMP",
            "description": "Легендарный финский отель с более чем столетней историей",
        },
    },
}
