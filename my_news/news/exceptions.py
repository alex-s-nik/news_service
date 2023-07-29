class BaseNewsException(BaseException):
    """Базовый класс исключения приложения News."""
    pass


class AlreadyLikedException(BaseException):
    """Исключение поднимается, если новость уже была лайкнута этим пользователем раньше."""
    pass
