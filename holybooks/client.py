from __future__ import annotations
from typing import TYPE_CHECKING
from .http import HTTPClient

if TYPE_CHECKING:
    from typing import Optional

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
    
    def fetch_surah(self, chapter_number: Optional[int, str]):
        return self.fetch_book_chapter(str(chapter_number))

    def fetch_ayat(self, citation: str, translation: str = ""):
        return self.fetch_chapter_verse(citation=citation, translation=translation)

    def fetch_chapter(self, book: str, chapter: Optional[int, str]):
        return self.fetch_book_chapter(chapter, book=book)
    
    def fetch_verse(self, book: str, citation: str, translation: str = ""):
        return self.fetch_chapter_verse(book, citation=citation, translation=translation)