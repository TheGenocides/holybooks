from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from typing import Union
    from .translation import QuranTranslation, BibleTranslation
    from ..constants import NUMBER

__all__ = (
    "Book",
    "Chapter",
    "Verse",
    "Translation"
)

@dataclass
class Translation:
    name: str
    id: NUMBER
    
class Comparable:
    def __eq__(self, other):
        o = getattr(self, "number", None)
        other= getattr("number", other, None)
        if o and other:
            return o == other and o.chapter == other.chapter and o.book == other.book
        return False
        
class Book(Comparable):
    def __init__(
        self, 
        name: str, 
        *,
        translation: Union[BibleTranslation, QuranTranslation]
    ) -> None:
        self.name = name
        self.translation = translation


class Chapter(Comparable):
    def __init__(
        self,
        number: int
    ) -> None:
        self.number = number

class Verse(Comparable):
    def __init__(
        self, 
        text: str,
        number: int
    ) -> None:
        self.text = text
        self.number = number

    