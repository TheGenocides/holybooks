from __future__ import annotations
from typing import TYPE_CHECKING
from .mixins import Book, Chapter, Verse
from .translation import QuranTranslation

if TYPE_CHECKING:
    from typing import Union, Optional


__all__ = (
    "Quran",
    "Surah",
    "Ayah"
)
class Quran(Book):
    def __init__(self, *args, **kwargs):
        self.data = kwargs.pop("data")
        self._surahs = [Surah(data=d) for d in self.data.get("surahs")]
        super().__init__("Quran", translation=QuranTranslation(**self.data.pop("translation")))

    def __repr__(self):
        return f"Quran(name={self.name}, surahs={self.surahs}, translation={self.translation})"

    def __str__(self):
        return self.name
        
    @property
    def surahs(self):
        return self._surahs

class Surah(Chapter):
    def __init__(self, *args, **kwargs):
        self.raw_data = kwargs.pop("data")
        self.data = self.raw_data.pop("data", None) or self.raw_data
        self.translation = QuranTranslation(**self.data.get("translation"))
        super().__init__(self.data.get("number"))

    def __repr__(self):
        return f"Surah(name={self.name}, number={self.number})"
        
    @property
    def name(self):
        return self.data.get("name")
        
    @property
    def english_name(self):
        return self.data.get("englishName")
        
    @property
    def english_name_translation(self):
        return self.data.get("englishNameTranslation")

    @property
    def revelation_type(self):
        return self.data.get("revelationType")

    @property
    def number_of_ayats(self):
        return self.data.get("numberOfAyahs") or len(self.ayats)

    @property
    def ayats(self):
        return [Ayah(data=data, surah=self) for data in self.data.get("ayahs")]

class Ayah(Verse):
    def __init__(self, *args, **kwargs):
        self.raw_data = kwargs.pop("data")
        self.data = self.raw_data.get("data") or self.raw_data
        self.translation = QuranTranslation(**self.data.get("translation"))
        self._surah = kwargs.pop("surah", None) or Surah(data=self.raw_data.get("surah") or self.data.get("surah"))
        super().__init__(self.data.get("text"), self.data.get("number"))

    def __repr__(self):
        return f"Ayah(number={self.number_in_surah}, surah={repr(self.surah)})"

    def __str__(self):
        return self.text

    @property
    def number_in_surah(self):
        return self.data.get("numberInSurah")

    @property
    def juz(self):
        return self.data.get("juz")
        
    @property
    def manzil(self):
        return self.data.get("manzil")
        
    @property
    def page(self):
        return self.data.get("page")
        
    @property
    def ruku(self):
        return self.data.get("ruku")

    @property
    def hizb_quarter(self):
        return self.data.get("hizbQuarter")

    @property
    def sajda(self):
        return self.data.get("sajda")

    @property
    def surah(self) -> Surah:
        return self._surah

# class Surah:
#     def __init__(self, surah: int = None):
#         self.surah = surah
#         self._session = None
#         self._async_session = None
#         self.data = None
#         self.ayah = None
#         self._request = None

#     @classmethod
#     def request(cls, surah: int = None):

#         self = cls(surah)

#         if not self._session:
#             self._session = requests.Session()

#         self._request = self._session.get(
#             f"https://api.alquran.cloud/v1/surah/{surah}/en.asad"
#         ).json()
#         self.data = self._request["data"]
#         self.ayah = self.data["ayahs"]
#         if self._request["code"] > 202:
#             raise ApiError(
#                 code=self._request["code"], msg=self._request["data"]
#             )

#         return self

#     @classmethod
#     async def async_request(cls, surah: int = None, *, loop=None):

#         self = cls(surah)

#         if not self._async_session:
#             self._async_session = aiohttp.ClientSession(loop=loop)

#         async with self._async_session as session:
#             async with session.get(
#                 f"https://api.alquran.cloud/v1/surah/{surah}/en.asad"
#             ) as resp:
#                 self._request = await resp.json()
#         self.data = self._request["data"]
#         self.ayah = self.data["ayahs"]
#         if self._request["code"] > 202:
#             raise ApiError(
#                 code=self._request["code"], msg=self._request["data"]
#             )
#         return self

#     @property
#     def api_code(self):
#         if not self._request:
#             return None
#         return self._request["code"]

#     @property
#     def api_status(self):
#         if not self._request:
#             return None
#         return self._request["status"]

#     def name(self, lang: str = "ar"):
#         if not self.data:
#             return None
#         if lang == "ar" or lang.lower() == "arabic":
#             return self.data["name"]

#         elif lang == "eng" or lang.lower() == "english":
#             return self.data["englishName"]

#         else:
#             raise WrongLang(lang=lang)

#     @property
#     def name_mean(self):
#         return self.data["englishNameTranslation"]

#     @property
#     def revelation_type(self):
#         return self.data["revelationType"]

#     @property
#     def number_ayahs(self):
#         return self.data["numberOfAyahs"]

#     def request_ayahs(self):
#         if not self.ayah:
#             return None
#         data = []
#         for number in range(Surah.request(self.surah).number_ayahs):
#             data.append(f"{self.ayah[number]['text']}")
#         return data

#     async def ayah_info(
#         self,
#         ayah: int = 1,
#         *,
#         text: bool = True,
#         number_in_quran: bool = True,
#         number_in_surah: bool = True,
#         juz: bool = True,
#         manzil: bool = True,
#         page: bool = True,
#         ruku: bool = True,
#         hizbquarter: bool = True,
#         sajda: bool = True,
#     ):
#         if ayah <= 0:
#             raise NumberError(
#                 mode=0, obj="ayah", first_query=1, second_query=None
#             )

#         elif ayah > int(Surah.request(self.surah).number_ayahs):
#             raise NumberError(
#                 mode=1,
#                 obj="ayah",
#                 first_query=1,
#                 second_query=Surah.request(self.surah).number_ayahs,
#             )

#         else:
#             ayah -= 1
#             data = {
#                 "text": self.ayah[ayah]["text"] if text else None,
#                 "number in quran": self.ayah[ayah]["number"]
#                 if number_in_quran
#                 else None,
#                 "number in surah": self.ayah[ayah]["numberInSurah"]
#                 if number_in_surah
#                 else None,
#                 "juz": self.ayah[ayah]["juz"] if juz else None,
#                 "manzil": self.ayah[ayah]["manzil"] if manzil else None,
#                 "page": self.ayah[ayah]["page"] if page else None,
#                 "ruku": self.ayah[ayah]["ruku"] if ruku else None,
#                 "hizbquarter": self.ayah[ayah]["hizbQuarter"]
#                 if hizbquarter
#                 else None,
#                 "sajda": self.ayah[ayah]["sajda"] if sajda else None,
#             }
#             return data

#     def __enter__(self):
#         return self

#     def __exit__(self, *args):
#         return

#     async def __aenter__(self):
#         return self

#     async def __aexit__(self, *args):
#         return

# class Ayah:
#     def __init__(self, surah: int = None, *, ayah: int = None):
#         self.surah = surah
#         self.ayah = ayah
#         self._request = None
#         self.data = None
#         self._session = None
#         self._async_session = None

#     @classmethod
#     def request(cls, surah: int = None, *, ayah: int = None, loop=None):
#         self = cls(surah, ayah=ayah)

#         if not self._session:
#             self._session = requests.Session()

#         self._request = self._session.get(
#             f"http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/en.asad"
#         ).json()
#         self.data = self._request["data"]
#         if self._request["code"] > 202:
#             raise ApiError(
#                 code=self._request["code"], msg=self._request["data"]
#             )
#         return self

#     @classmethod
#     async def async_request(
#         cls, surah: int = None, *, ayah: int = None, loop=None
#     ):

#         self = cls(surah, ayah=ayah)

#         if not self._async_session:
#             self._async_session = aiohttp.ClientSession(loop=loop)

#         try:
#             async with self._async_session as session:
#                 async with session.get(
#                     f"http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/en.asad"
#                 ) as resp:
#                     self._request = await resp.json()
#         except aiohttp.client_exceptions.ContentTypeError:
#             raise ContentTypeError(
#                 class_="Ayah",
#                 mode="ayah",
#                 first_query=surah,
#                 second_query=surah,
#             )

#         self.data = self._request["data"]
#         if self._request["code"] > 202:
#             raise ApiError(
#                 code=self._request["code"], msg=self._request["data"]
#             )
#         return self

#     @property
#     def api_code(self):
#         if not self._request:
#             return None
#         return self._request["code"]

#     @property
#     def api_status(self):
#         if not self._request:
#             return None
#         return self._request["status"]

#     def __enter__(self):
#         return self

#     def __exit__(self, *args):
#         return

#     async def __aenter__(self):
#         return self

#     async def __aexit__(self, *args):
#         return

# class Search:
#     def __init__(
#         self,
#         mention: str = None,
#         *,
#         surah: Optional[Union[str, int]] = None,
#         request: int = None,
#     ):
#         self.mention = mention
#         self.surah = surah
#         self.req = request
#         self.data = None
#         self.matches = None
#         self._session = self._async_session = None
#         self._request = None

#     @classmethod
#     async def async_request(
#         cls,
#         mention: str = None,
#         *,
#         surah: Optional[Union[str, int]] = None,
#         request: int = None,
#         loop=None,
#     ):

#         self = cls(mention, surah=surah, request=request)

#         if not self._async_session:
#             self._async_session = aiohttp.ClientSession(loop=loop)

#         try:
#             async with self._async_session as session:
#                 async with session.get(
#                     f"http://api.alquran.cloud/v1/search/{mention}/{surah}/en.pickthall"
#                 ) as resp:
#                     self._request = await resp.json()
#         except aiohttp.client_exceptions.ContentTypeError:
#             raise ContentTypeError(
#                 class_="Search",
#                 mode="search",
#                 first_query=mention,
#                 second_query=surah,
#             )

#         self.data = self._request["data"]
#         self.matches = self.data["matches"]
#         if self._request["code"] > 202:
#             raise ApiError(
#                 code=self._request["code"], msg=self._request["data"]
#             )

#         return self

#     @classmethod
#     def request(
#         cls,
#         mention: str = None,
#         *,
#         surah: Optional[Union[str, int]] = None,
#         request: int = None,
#     ):

#         self = cls(mention, surah=surah, request=request)

#         if not self._session:
#             self._session = requests.Session()

#         self._request = self._session.get(
#             f"http://api.alquran.cloud/v1/search/{mention}/{surah}/en.pickthall"
#         ).json()
#         self.data = self._request["data"]
#         self.matches = self.data["matches"]
#         if self._request["code"] > 202:
#             raise ApiError(
#                 code=self._request["code"], msg=self._request["data"]
#             )
#         return self

#     @property
#     def count(self):
#         if not self.data:
#             return None
#         return self.data["count"]

#     @property
#     def api_code(self):
#         if not self._request:
#             return None
#         return self._request["code"]

#     @property
#     def api_status(self):
#         if not self._request:
#             return None
#         return self._request["status"]

#     def find(self):
#         if self.data is None or self.matches is None:
#             return None
#         data = []
#         if self.req is None:
#             for num in range(self.data["count"]):
#                 data.append(self.matches[num]["text"])

#         else:
#             for num in range(self.req):
#                 data.append(self.matches[num]["text"])
#         return data

#     def __enter__(self):
#         return self

#     def __exit__(self, *args):
#         return

#     async def __aenter__(self):
#         return self

#     async def __aexit__(self, *args):
#         return
