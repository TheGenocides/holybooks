from .bible import Bible
from .errors import ApiError, NotFound, BibleOnly

__all__ = ("Torah",)


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
