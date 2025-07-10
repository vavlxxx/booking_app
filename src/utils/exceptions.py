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
    detail = "Дата заезда не может быть равна или быть позже даты выезда"

class CurrentDateException(ApplicationBaseException):
    detail = "Нельзя начать бронь в день въезда"

class NotEmptyHotelException(ApplicationBaseException):
    detail = "Невозможно удалить отель, у которого есть номера"

class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"

class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class ApplicationBaseHTTPException(HTTPException):
    detail = "Возникла ошибка на стороне сервера"
    status_code = 500
    status = "ERROR"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(ApplicationBaseHTTPException):
    detail = "Отель не найден"
    status_code = 404
    
class RoomNotFoundHTTPException(ApplicationBaseHTTPException):
    detail = "Номер не найден"
    status_code = 404

class InvalidDataHTTPException(ApplicationBaseHTTPException):
    detail = "Переданы некорректные данные"
    status_code = 400

class NotEmptyHotelHTTPException(ApplicationBaseHTTPException):
    detail = "Нельзя удалить отель с номерами"
    status_code = 422

class DatesMissMatchHTTPException(ApplicationBaseHTTPException):
    detail = "Дата заезда не может быть равна или быть позже даты выезда"
    status_code = 422

class CurrentDateHTTPException(ApplicationBaseHTTPException):
    detail = "Нельзя начать бронь в день въезда"
    status_code = 422
