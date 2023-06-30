from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Union

__all__ = (
    "ApiError",
    "ContentTypeError",
    "NumberError",
    "WrongLang",
    "NotFound",
    "TooManyRequests",
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
    def __init__(self, msg) -> None:
        super().__init__(msg)


class TooManyRequests(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Too many requests!"
        )
