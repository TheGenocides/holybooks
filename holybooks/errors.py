from typing import TYPE_CHECKING
from typing import Optional, Union

__all__ = (
    "ApiError",
    "ContentTypeError",
    "NumberError",
    "WrongLang",
    "NotFound",
    "BibleOnly",
)


class ApiError(Exception):
    def __init__(self, status: int, msg: str) -> None:
        super().__init__(f"Api has an error, return code: {status}.\n{msg}")


class ContentTypeError(Exception):
    def __init__(
        self,
        class_: str,
        mode: str,
        first_query: Optional[Union[str, int]],
        second_query: Optional[Union[str, int]],
    ) -> None:
        super().__init__(
            f"Attempt to decode JSON with unexpected mimetype: Return code: None\nlink: http://api.alquran.cloud/v1/{mode}/{first_query}:{second_query}/en.asad"
            if class_ == "Ayah"
            else f"Attempt to decode JSON with unexpected mimetype: Return code: None\nlink: http://api.alquran.cloud/v1/{mode}/{first_query}/{second_query}/en.asad"
        )


class NumberError(Exception):
    def __init__(
        self,
        mode: int,
        obj: str,
        first_query: int,
        second_query: Optional[Union[str, int]],
    ) -> None:
        super().__init__(
            f"{obj} must above {first_query}"
            if mode == 0
            else f"{obj} must be between {first_query} to {second_query}"
        )


class WrongLang(Exception):
    def __init__(self, lang: str) -> None:
        super().__init__(
            f"The lang '{lang}' is not supported, it only support arabic(ar) and english(eng)"
        )


class NotFound(Exception):
    def __init__(self, book: str, chapter: int, verse: str) -> None:
        super().__init__(
            f"Book {book}, Chapter {chapter}, Verse(s) {verse} Wasn't Found."
        )


class BibleOnly(Exception):
    def __init__(self, book: str) -> None:
        super().__init__(
            f"The book {book} wasn't found because its available only in Bible"
        )
