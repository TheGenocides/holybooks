from __future__ import annotations

import requests

from typing import TYPE_CHECKING
from .quran import Quran, Surah, Ayah
from .bible import BibleChapter, BibleVerse
from .errors import NotFound, TooManyRequests
from .constants import SLASH

if TYPE_CHECKING:
    from .constants import Number 
    



__all__ = (
    "HTTPClient",
)

class HTTPClient:
    def __init__(self, *, quran_translation = "en.asad", bible_translation = "kjv"):
        self.quran_translation = quran_translation
        self.bible_translation = bible_translation
        self.base_quran_url = "http://api.alquran.cloud/v1"
        self.base_bible_url = "https://bible-api.com"
        self.urls = {
            "quran": {
                "quran": lambda translation = self.quran_translation: self.base_quran_url + "/quran" + SLASH + translation,
                "chapter": lambda chapter, translation = self.quran_translation: self.base_quran_url + "/surah/" + str(chapter) + SLASH + translation,
                "verse": lambda citation, translation = self.quran_translation: self.base_quran_url + "/ayah/" + citation + SLASH + translation,
                "search": lambda keyword, surah = "all", translation = self.quran_translation: self.base_quran_url + "/search/" + keyword + SLASH + surah + SLASH + translation,
                "juz": lambda juz, translation = self.quran_translation: self.base_quran_url + "/juz/" + str(juz) + SLASH + translation,
                "manzil": lambda manzil, translation = self.quran_translation: self.base_quran_url + "/manzil/" + str(manzil) + SLASH + translation,
                "ruku": lambda ruku, translation = self.quran_translation: self.base_quran_url + "/ruku/" + str(ruku) + SLASH + translation,
                "page": lambda page, translation = self.quran_translation: self.base_quran_url + "/page/" + str(page) + SLASH + translation,
                "hizb_quarter": lambda hizb_quarter, translation = self.quran_translation: self.base_quran_url + "/hizbQuarter/" + str(hizb_quarter) + SLASH + translation,
                "sajda": lambda translation = self.quran_translation: self.base_quran_url + "/sajda/" +  SLASH + translation
            },
            "bible": {
                "chapter": lambda book, chapter, translation = self.bible_translation: self.base_bible_url + SLASH + book + str(chapter) + f"?translation={translation}",
                "verse": lambda book, chapter, starting_verse, ending_verse = "", translation = self.bible_translation: self.base_bible_url + SLASH + book + str(chapter) + ":" + str(starting_verse) + ("-" + str(ending_verse) if str(ending_verse) else "") + f"?translation={translation}"
            }
        }
        self.__session = requests.Session()

    def _parse_ayahs(self, res):
        edition = res["data"]["edition"]
        data = res.get("data")
        verses = data.get("ayahs") or None
            
        if verses:
            for verse in verses:
                verse["translation"] = edition
                surah = verse.get("surah")
                if surah:
                    surah["translation"] = edition
            res["data"]["translation"] = edition
            return res, 1
        else:
            res["data"]["translation"] = edition
            surah = res.get("data").get("surah")
            if surah:
                surah["translation"] = edition
            return res, 0
        

    def request(
        self,
        url: str,
        method: str = "get",
        *args,
        **kwargs
    ):
        try: 
            req = getattr(self.__session, method.lower())
        except AttributeError:
            raise AttributeError(f"Cannot find method: {method}")

        url = url.replace(" ", "%20")
        res = req(url, *args, **kwargs)
        data = res.json()
        code = res.status_code
        if code == 204:
            return None
                
        elif code == 404:
            try:
                raise NotFound(data["data"])
            except KeyError:
                raise NotFound(data["error"])
            except TypeError:
                raise NotFound(data)

        elif code == 429:
            raise TooManyRequests()
        return data

    def fetch_book(self, book: str = "", *, translation: str = ""):
        if book:
            ... #TODO: For bible later!

        else:
            url = self.urls["quran"]["quran"](translation if translation else self.quran_translation)
            res = self.request(url)
            edition = res["data"]["edition"]
            res["data"]["translation"] = edition
            for chapter in res["data"]["surahs"]:
                chapter["translation"] = edition 
            return Quran(**res, session=self.__session)

    def fetch_book_chapter(
        self, 
        chapter, 
        *, 
        book: str = "", 
        beginning_verse: Number = "",
        ending_verse: Number = "",
        translation = ""
    ):
        if book:
            url = self.urls["bible"]["chapter"](book, chapter, translation or self.bible_translation)
            res = self.request(url)
            verses = res["verses"]
            translation_data = {
                "name": res["translation_name"],
                "id": res["translation_id"],
                "note": res["translation_note"]
            }
            for verse in verses:
                verse["translation"] = translation_data
                verse["reference"] = res["reference"]
            res["translation"] = translation_data
            _verse = verses[0]
            res["book_name"] = _verse["book_name"]
            res["book_id"] = _verse["book_id"]
            del res["translation_name"]
            del res["translation_id"]
            del res["translation_note"]
            res["number"] = _verse["chapter"]
            return BibleChapter(**res)
        
        else:
            url = self.urls["quran"]["chapter"](chapter, translation or self.quran_translation)
            res = self.request(url)
            res = self._parse_ayahs(res)[0]
            return Surah(data=res, session=self.__session)

    def fetch_chapter_verse(
        self, 
        book: str = "", 
        *,
        citation: str,
        translation: str = "",
        **kwargs
    ):
        if book:
            try:
                chapter, verse = citation.split(":")
                if "-" in verse:
                    starting_verse, ending_verse = verse.split("-")

                else:
                    starting_verse, ending_verse = (verse, "")
            except ValueError:
                raise ValueError("Wrong citation! the citation argument must be put with any of these formats: 1:1, 3:10, 3:1-10")
                
            url = self.urls["bible"]["verse"](book, chapter, starting_verse, ending_verse, translation or self.bible_translation)
            res = self.request(url)
            data = res["verses"]
            if len(data) > 1:
                for d in data:
                    d["reference"] = res["reference"]
                    d["translation"] = {
                        "name": res["translation_name"],
                        "id": res["translation_id"],
                        "note": res["translation_note"]
                    }
                    
                return [BibleVerse(**d) for d in data]
            
            else:
                # if
                data = data[0]
                data["reference"] = res["reference"]
                data["translation"] = {
                    "name": res["translation_name"],
                    "id": res["translation_id"],
                    "note": res["translation_note"]
                }
                
                return BibleVerse(**data)

        else:
            params = {}
            offset = kwargs.pop("offset", None)
            limit = kwargs.pop("limit", None)
            juz = kwargs.pop("juz", None)
            manzil = kwargs.pop("manzil", None)
            ruku = kwargs.pop("ruku", None)
            page = kwargs.pop("page", None)
            hizb_quarter = kwargs.pop("hizb_quarter", None)
            sajda = kwargs.pop("sajda", None)
            
            if juz:
                url = self.urls["quran"]["juz"](juz, translation or self.quran_translation)
            
            elif manzil:
                url = self.urls["quran"]["manzil"](manzil, translation or self.quran_translation)

            elif ruku:
                url = self.urls["quran"]["ruku"](ruku, translation or self.quran_translation)

            elif page:
                url = self.urls["quran"]["page"](page, translation or self.quran_translation)

            elif hizb_quarter:
                url = self.urls["quran"]["hizb_quarter"](hizb_quarter, translation or self.quran_translation)

            elif sajda:
                url = self.urls["quran"]["sajda"](translation or self.quran_translation)
                
            else:
                url = self.urls["quran"]["verse"](citation, translation or self.quran_translation)

            if offset:
                params["offset"] = offset
            
            if limit:
                params["limit"] = limit
                
            res = self.request(url, params=params)
            data, check = self._parse_ayahs(res)
            if not check:
                return Ayah(data=data, session=self.__session)
            return [Ayah(data=verse, session=self.__session) for verse in data["data"]["ayahs"]]

    def search(self, keyword: str, chapter: Number = "all", translation: str = ""):
        url = self.urls["quran"]["search"](keyword, chapter, translation or self.quran_translation)
        data = self.request(url)
        verses = data["data"]["matches"]
        for verse in verses:
            verse["translation"] = verse["edition"]
            verse["surah"]["translation"] = verse["edition"]
        return [Ayah(data=d) for d in verses]

