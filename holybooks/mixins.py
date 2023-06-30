from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from typing import List, Optional
    from .translation import QuranTranslation, BibleTranslation

__all__ = (
    "Book",
    "Chapter",
    "Verse",
    "Translation"
)

@dataclass
class Translation:
    name: str
    id: str
    
class Comparable:
    def __eq__(self, other):
        o = getattr("number", self, None)
        other= getattr("number", other, None)
        if o and other:
            return o == other and o.chapter == other.chapter and o.book == other.book
        return False
        
class Book(Comparable):
    def __init__(
        self, 
        name: str, 
        *,
        translation: Optional[Translation, BibleTranslation, QuranTranslation]
    ):
        self.name = name
        self.translation = translation


class Chapter(Comparable):
    def __init__(
        self,
        number: int
    ):
        self.number = number
        # self.verse = verse

class Verse(Comparable):
    def __init__(
        self, 
        text: str,
        number: int
    ):
        self.text = text
        self.number = number

    