class ApiError(Exception):
    def __init__(self, status: int, msg: str) -> None:
        super().__init__(f"Api has an error, return code: {status}.\n{msg}")


class NotFound(Exception):
    def __init__(self, book: str, chapter: int, verse: str) -> None:
        super().__init__(
            f"Book {book}, Chapter {chapter}, Verse(s) {verse} Wasn't Found."
        )


class ApiError(Exception):
    pass


class NumberError(Exception):
    pass


class WrongLang(Exception):
    pass
