class BaseException(Exception):
    """Classe base para exceções customizadas da aplicação."""
    message: str = "Internal Server Error"

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message
        super().__init__(message)


class NotFoundException(BaseException):
    """Exceção para quando um recurso não é encontrado."""
    message: str = "Resource not found"