from .errors import ApiError, NotFound
import aiohttp
import requests

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
        self._session = None
        self._async_session = None
        self.json = None
        self.verses = None
        self.raw_verse = None
        self._request = None

    @classmethod
    def request(
        cls,
        book: str,
        *,
        chapter: int,
        starting_verse: int,
        ending_verse: int = None,
    ):

        self = cls(book)
        verse = _build_verse(starting_verse, ending_verse)

        if not self._session:
            self._session = requests.Session()

        self._request = self._session.get(
            f"https://bible-api.com/{book}+{chapter}:{verse}"
        )
        if self._request.status_code == 404:
            raise NotFound(book, chapter, verse)
        elif self._request.status_code > 202:
            raise ApiError(
                self._request.status_code,
                self._request.json().get("error", ""),
            )

        self.json = self._request.json()
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

        self = cls(book)
        verse = _build_verse(starting_verse, ending_verse)

        if not self._async_session:
            self._async_session = aiohttp.ClientSession(loop=loop)

        async with self._async_session as session:
            async with session.get(
                f"https://bible-api.com/{book}+{chapter}:{verse}"
            ) as resp:
                self._request = resp
                self.json = await resp.json()

        self.verses = [ChapterVerse(i) for i in self.json["verses"]]
        self.raw_verse = self.json["text"]
        if self._request.status == 404:
            raise NotFound(book, chapter, verse)
        elif self._request.status > 202:
            raise ApiError(self._request.status, self.json.get("error", ""))

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
