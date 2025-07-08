
class ApplicationBaseException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ObjectNotFoundException(ApplicationBaseException):
    detail = "Объект не найден"

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
