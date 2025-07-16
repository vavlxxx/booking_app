from typing import Dict
from fastapi.openapi.models import Example

USER_REGISTER_EXAMPLES: Dict[str, Example] = {
    "ANNA_SMITH": {
        "summary": "Анна Смит - Менеджер",
        "value": {
            "first_name": "Анна",
            "last_name": "Смит",
            "birthday": "1985-03-15",
            "gender": "Ж"
        }
    },
    "JOHN_JOHNSON": {
        "summary": "Джон Джонсон - Разработчик",
        "value": {
            "first_name": "Джон",
            "last_name": "Джонсон",
            "birthday": "1990-07-22",
            "gender": "М"
        }
    },
    "MARIA_GARCIA": {
        "summary": "Мария Гарсия - Дизайнер",
        "value": {
            "first_name": "Мария",
            "last_name": "Гарсия",
            "birthday": "1992-11-08",
            "gender": "Ж"
        }
    },
    "ALEX_PETROV": {
        "summary": "Алекс Петров - Аналитик",
        "value": {
            "first_name": "Алекс",
            "last_name": "Петров",
            "birthday": "1988-05-30",
            "gender": "М"
        }
    },
    "ELENA_VOLKOV": {
        "summary": "Елена Волкова - Маркетолог",
        "value": {
            "first_name": "Елена",
            "last_name": "Волкова",
            "birthday": "1995-12-14",
            "gender": "Ж"
        }
    }
}



USER_LOGIN_EXAMPLES: Dict[str, Example] = {
    "ANNA_SMITH": {
        "summary": "Анна Смит - Менеджер",
        "value": {
            "email": "anna.smith@example.com",
            "password": "SecurePass123"
        }
    },
    "JOHN_JOHNSON": {
        "summary": "Джон Джонсон - Разработчик",
        "value": {
            "email": "john.johnson@techcorp.com",
            "password": "DevPassword456"
        }
    },
    "MARIA_GARCIA": {
        "summary": "Мария Гарсия - Дизайнер",
        "value": {
            "email": "maria.garcia@creative.studio",
            "password": "Design789Pass"
        }
    },
    "ALEX_PETROV": {
        "summary": "Алекс Петров - Аналитик",
        "value": {
            "email": "alex.petrov@datacompany.ru",
            "password": "Analytics2024"
        }
    },
    "ELENA_VOLKOV": {
        "summary": "Елена Волкова - Маркетолог",
        "value": {
            "email": "elena.volkov@marketing.pro",
            "password": "Marketing321"
        }
    }
}
