from __future__ import annotations
from typing import TYPE_CHECKING
from .http import HTTPClient
from .models import Quran, Surah, Ayah, BibleChapter, BibleVerse

if TYPE_CHECKING:
    from typing import Optional, Union, List
    from .constants import NUMBER
    from .models import Quran, Surah, Ayah, BibleChapter, BibleVerse

__all__ = (
    "Client",
)

class Client:
    def __init__(self, *, quran_translation: str = "en.asad", bible_translation: str = "kjv") -> None:
        self.quran_translation = quran_translation
        self.bible_translation = bible_translation
        self.http_client = HTTPClient(quran_translation = self.quran_translation,
            bible_translation = self.bible_translation)

    def fetch_quran(self, translation: str = "") -> Quran:
        return Quran(**self.http_client.fetch_book(translation=translation))
    
    def fetch_surah(self, chapter: NUMBER, translation: str = "") -> Surah:
        return Surah(**self.http_client.fetch_book_chapter(str(chapter), translation=translation))

    def fetch_ayah(self, citation: str = "", translation: str = "", *, juz: NUMBER = None, manzil: NUMBER = None, ruku: NUMBER = None, page: NUMBER = None, hizb_quarter: NUMBER = None, sajda: bool = False, offset: NUMBER = None, limit: NUMBER = None) -> Union[Ayah, List[Ayah]]:
        data = self.http_client.fetch_chapter_verse(
            citation=citation, 
            translation=translation,
            juz=juz,
            manzil=manzil, 
            sajda=sajda,
            ruku=ruku,
            page=page,
            hizb_quarter=hizb_quarter,
            offset=offset,
            limit=limit
        )

        if isinstance(data, dict):
            return Ayah(**data)
        return [Ayah(**d) for d in data]

    def fetch_chapter(self, book: str, chapter: NUMBER) -> BibleChapter:
        return BibleChapter(self.http_client.fetch_book_chapter(chapter, book=book))
    
    def fetch_verse(self, book: str, citation: str, translation: str = "") -> Union[BibleVerse, List[BibleVerse]]:
        data = self.http_client.fetch_chapter_verse(book, citation=citation, translation=translation)
        if isinstance(data, dict):
            return BibleVerse(**data)
        return [BibleVerse(**d) for d in data]