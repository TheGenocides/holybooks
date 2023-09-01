from __future__ import annotations

import requests

from typing import TYPE_CHECKING
from dataclasses import dataclass
from .mixins import Book, Chapter, Verse
from .translation import QuranTranslation

if TYPE_CHECKING:
    from typing import Union, Optional, List, Self
    from io import BufferedWriter
    from ..constants import NUMBER


__all__ = (
    "Quran",
    "Surah",
    "Ayah"
)

@dataclass
class Sajda:
    id: NUMBER
    recommended: bool
    obligatory: bool

class Quran(Book):
    def __init__(self, *args, **kwargs) -> None:
        self.data = kwargs.pop("data")
        self.__session = kwargs.get("session", requests.Session())
        self._surahs = [Surah(data=d, session=self.__session) for d in self.data.get("surahs")]
        super().__init__("Quran", translation=QuranTranslation(**self.data.pop("translation")))

    def __repr__(self):
        return f"Quran(name={self.name}, surahs={self.surahs}, translation={self.translation})"

    def __str__(self):
        return self.name
        
    @property
    def surahs(self) -> Optional[List[Surah]]:
        return self._surahs

class Surah(Chapter):
    def __init__(self, *args, **kwargs) -> None:
        self.raw_data = kwargs.pop("data")
        self.data = self.raw_data.pop("data", None) or self.raw_data
        self.translation = QuranTranslation(**self.data.get("translation"))
        self.__session = kwargs.get("session", None)
        super().__init__(self.data.get("number"))

    def __repr__(self):
        return f"Surah(name={self.name}, number={self.number})"
        
    @property
    def name(self) -> str:
        return self.data.get("name")
        
    @property
    def english_name(self) -> str:
        return self.data.get("englishName")
        
    @property
    def english_name_translation(self) -> str:
        return self.data.get("englishNameTranslation")

    @property
    def revelation_type(self) -> str:
        return self.data.get("revelationType")

    @property
    def number_of_ayats(self) -> NUMBER:
        return self.data.get("numberOfAyahs") or len(self.ayats)

    @property
    def ayats(self) -> List[Ayah]:
        return [Ayah(data=data, surah=self, session=self.__session) for data in self.data.get("ayahs")]

class Ayah(Verse):
    def __init__(self, *args, **kwargs) -> None:
        self.raw_data = kwargs.pop("data")
        self.data = self.raw_data.get("data") or self.raw_data
        self.translation = QuranTranslation(**self.data.get("translation"))
        self.__session = kwargs.get("session", requests.Session())
        self._surah = kwargs.pop("surah", None) or Surah(data=self.raw_data.get("surah") or self.data.get("surah"), session=self.__session)
        super().__init__(self.data.get("text"), self.data.get("number"))

    def __repr__(self):
        return f"Ayah(number={self.number_in_surah}, surah={repr(self.surah)})"

    def __str__(self):
        return self.text

    def download_audio(self, filename: str = "", ext: str = "mp3") -> Optional[BufferedWriter]:
        if not self.audio:
            return None
        with open(filename + "." +  ext or f"{self.surah.number}:{self.number_in_surah}.{ext}", "wb") as f:
            f.write(self.__session.get(self.audio).content)
        return f
        
    @property
    def audio(self) -> Optional[str]:
        return self.data.get("audio")

    @property
    def number_in_surah(self) -> int:
        return int(self.data.get("numberInSurah"))

    @property
    def juz(self) -> int:
        return int(self.data.get("juz"))
        
    @property
    def manzil(self) -> int:
        return int(self.data.get("manzil"))
        
    @property
    def page(self) -> int:
        return int(self.data.get("page"))
        
    @property
    def ruku(self) -> int:
        return int(self.data.get("ruku"))

    @property
    def hizb_quarter(self) -> int:
        return int(self.data.get("hizbQuarter"))

    @property
    def sajda(self) -> Union[bool, Sajda]:
        data = self.data.get("sajda")
        return False if not data else Sajda(**data)
    
    @property
    def surah(self) -> Surah:
        return self._surah