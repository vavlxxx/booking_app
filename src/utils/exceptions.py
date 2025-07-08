
class ApplicationBaseException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ObjectNotFoundException(ApplicationBaseException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(ApplicationBaseException):
    detail = "Не осталось свободных номеров"
