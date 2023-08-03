from __future__ import annotations
from typing import TYPE_CHECKING

from .mixins import Book, Chapter, Verse
from .translation import BibleTranslation

if TYPE_CHECKING:
    from typing import List, Optional

__all__ = (
    "BibleBook", 
    "BibleChapter", 
    "BibleVerse"
)

class BibleBook(Book):
    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop("id")
        self.chapter = kwargs.pop("chapter")
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"BibleBook(name={self.name}, chapter={self.chapter}, translation={self.translation})"

    def __str__(self):
        return self.name

class BibleChapter(Chapter):
    def __init__(self, *args, **kwargs):
        self.verse = kwargs.pop("verse", None)
        self.verses = [BibleVerse(**data) for data in kwargs.pop("verses")] if kwargs.get("verses", None) else None
        self.book_name = kwargs.pop("book_name")
        self.book_id = kwargs.pop("book_id")
        self.reference = kwargs.pop("reference", None)
        self.full_text = kwargs.pop("text", None)
        if not isinstance(kwargs.get("translation"), BibleTranslation):
            self.translation = BibleTranslation(**kwargs.pop("translation"))
            
        else:
            self.translation = kwargs.pop("translation")
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"BibleChapter(number={self.number}, book={self.book.name})"

    def __str__(self):
        return self.book.name
        
    @property
    def book(self) -> BibleBook:
        return BibleBook(
            self.book_name, 
            translation=self.translation, 
            chapter=self, 
            id=self.book_id
        )


class BibleVerse(Verse):
    def __init__(self, *args, **kwargs):
        self.book_id = kwargs.pop("book_id")
        self.book_name = kwargs.pop("book_name")
        self.chapter_number = kwargs.pop("chapter")
        self.reference = kwargs.pop("reference")
        self.translation = BibleTranslation(**kwargs.pop("translation"))
        super().__init__(
            text=kwargs.get("text"), 
            number=kwargs.get("verse")
        )

    def __repr__(self) -> str:
        return f"BibleVerse(number={self.number}, chapter={repr(self.chapter)}, reference={self.reference})"

    def __str__(self) -> str:
        return self.text

    @property
    def book(self) -> BibleBook:
        return self.chapter.book

    @property
    def chapter(self) -> BibleChapter:
        return BibleChapter(
            self.chapter_number, 
            verse=self, 
            book_name=self.book_name, 
            book_id=self.book_id,
            translation=self.translation
        ) 