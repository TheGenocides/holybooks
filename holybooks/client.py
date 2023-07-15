from __future__ import annotations
from typing import TYPE_CHECKING
from .http import HTTPClient

if TYPE_CHECKING:
    from .constants import Number

__all__ = (
    "Client",
)

class Client(HTTPClient):
    def __init__(self, *, quran_translation: str = "en.asad", bible_translation: str = "kjv"):
        self.quran_translation = quran_translation
        self.bible_translation = bible_translation
        super().__init__(
            quran_translation = self.quran_translation,
            bible_translation = self.bible_translation
        )

    def fetch_quran(self, translation: str = ""):
        return self.fetch_book(translation=translation)
    
    def fetch_surah(self, chapter: Number, translation: str = ""):
        return self.fetch_book_chapter(str(chapter), translation=translation)

    def fetch_ayah(self, citation: str = "", translation: str = "", *, juz: Number = None, manzil: Number = None, ruku: Number = None, page: Number = None, hizb_quarter: Number = None, sajda: bool = False, offset: Number = None, limit: Number = None):
        return self.fetch_chapter_verse(
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

    def fetch_chapter(self, book: str, chapter: Number):
        return self.fetch_book_chapter(chapter, book=book)
    
    def fetch_verse(self, book: str, citation: str, translation: str = ""):
        return self.fetch_chapter_verse(book, citation=citation, translation=translation)