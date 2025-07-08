from fastapi import HTTPException


class ApplicationBaseException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ObjectNotFoundException(ApplicationBaseException):
    detail = "Объект не найден"

class ObjectAlreadyExistsException(ApplicationBaseException):
    detail = "Объект уже существует"

class InvalidDataException(ApplicationBaseException):
    detail = "Некорректные данные"

class AllRoomsAreBookedException(ApplicationBaseException):
    detail = "Не осталось свободных номеров"

class NotAuthenticatedException(ApplicationBaseException):
    detail = "Пользователь не аутентифицирован"

class UserAlreadyExistsException(ApplicationBaseException):
    detail = "Пользователь с таким email уже зарегистрирован"

class DatesMissMatchException(ApplicationBaseException):
    detail = "Дата заезда не может быть позже даты выезда"

class CurrentDateException(ApplicationBaseException):
    detail = "Нельзя начать бронь в день въезда"


class ApplicationBaseHTTPException(HTTPException):
    detail = None
    status_code = 500

    def __init__(self, *args: object) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail, *args)


class HotelNotFoundHTTPException(ApplicationBaseHTTPException):
    detail = "Отель не найден"
    status_code = 404

class RoomNotFoundHTTPException(ApplicationBaseHTTPException):
    detail = "Номер не найден"
    status_code = 404

class InvalidDataHTTPException(ApplicationBaseHTTPException):
    detail = "Переданы некорректные данные"
    status_code = 400
