from .errors import ApiError, NotFound

__all__ = ("ChapterVerse", "Bible")


def _build_verse(start: int, end: int = None) -> str:
    return f"{start}{f'-{end}' if end else ''}"


def _build_citation(book: str, chapter: int, verse: str) -> str:
    return f"{book} {chapter}:{verse}"


class ChapterVerse:
    def __init__(self, verse: dict) -> None:
        del verse["book_id"]

        for key, val in verse.items():
            setattr(self, key, val)

    def __str__(self) -> str:
        return self.text

    @property
    def citation(self) -> str:
        return _build_citation(self.book_name, self.chapter, self.verse)


class Bible:
    def __init__(self, book: str) -> None:
        self.book = book

    @classmethod
    def request(
        cls,
        book: str,
        *,
        chapter: int,
        starting_verse: int,
        ending_verse: int = None,
    ):
        try:
            import requests
        except ImportError:
            raise ImportError(
                "Please Install the requests module if you want to make a sync request."
            )

        self = cls(book)
        verse = _build_verse(starting_verse, ending_verse)

        self.request = requests.get(
            f"https://bible-api.com/{book}+{chapter}:{verse}"
        )
        if self.request.status_code == 404:
            raise NotFound(book, chapter, verse)
        elif self.request.status_code > 202:
            raise ApiError(
                self.request.status_code, self.request.json().get("error", "")
            )

        self.json = self.request.json()
        self.verses = [ChapterVerse(i) for i in self.json["verses"]]

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
        try:
            import aiohttp
        except ImportError:
            raise ImportError(
                "Please Install the aiohttp module if you want to make an async request."
            )

        self = cls(book)
        verse = _build_verse(starting_verse, ending_verse)

        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.get(
                f"https://bible-api.com/{book}+{chapter}:{verse}"
            ) as resp:
                self.request = resp
                self.json = await resp.json()

        self.verses = [ChapterVerse(i) for i in self.json["verses"]]
        self.raw_verse = self.json["text"]
        if self.request.status == 404:
            raise NotFound(book, chapter, verse)
        elif self.request.status > 202:
            raise ApiError(self.request.status, self.json.get("error", ""))

        return self

    @property
    def citation(self) -> str:
        return self.json["reference"]

    @property
    def translation(self) -> str:
        return self.json["translation_name"]
