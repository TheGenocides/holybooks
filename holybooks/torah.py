from .bible import Bible
from .errors import BibleOnly

__all__ = ("Torah",)


class Torah(Bible):
    def __init__(self, book: str) -> None:
        super().__init__(book)

    @classmethod
    def request(
        cls,
        book: str,
        *,
        chapter: int,
        starting_verse: int,
        ending_verse: int = None,
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
        if not self.json:
            return None
        return self.json["reference"]

    @property
    def translation(self) -> str:
        if not self.json:
            return None
        return self.json["translation_name"]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return
