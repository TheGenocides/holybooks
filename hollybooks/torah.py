from .bible import Bible


__all__ = ("ApiError", "NotFound", "Torah", "BibleOnly")


class ApiError(Exception):
    def __init__(self, status: int, msg: str) -> None:
        super().__init__(f"Api has an error, return code: {status}.\n{msg}")


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


class Torah(Bible):
    def __init__(self, book: str) -> None:
        super().__init__(book)

    @classmethod
    def request(
        cls, book: str, *, chapter: int, starting_verse: int, ending_verse: int = None
    ):
        if book.lower() not in [
            "genesis",
            "exodus",
            "leviticus",
            "numbers",
            "deuteronomy",
        ]:
            raise BibleOnly(book)

        self = super(Torah, cls).request(
            book,
            chapter=chapter,
            starting_verse=starting_verse,
            ending_verse=ending_verse,
        )

        return self

    @classmethod
    async def async_request(
        cls,
        book: str,
        *,
        chapter: int,
        starting_verse: int,
        ending_verse: int = None,
        loop=None,
    ):
        if book.lower() not in [
            "genesis",
            "exodus",
            "leviticus",
            "numbers",
            "deuteronomy",
        ]:
            raise BibleOnly(book)

        self = await super(Torah, cls).async_request(
            book,
            chapter=chapter,
            starting_verse=starting_verse,
            ending_verse=ending_verse,
            loop=loop,
        )

        return self

    @property
    def citation(self) -> str:
        return self.json["reference"]

    @property
    def translation(self) -> str:
        return self.json["translation_name"]
