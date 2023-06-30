from __future__ import annotations

import requests

from typing import TYPE_CHECKING
from .quran import Quran, Surah, Ayah
from .bible import BibleChapter, BibleVerse
from .errors import NotFound, TooManyRequests

if TYPE_CHECKING:
    from typing import Optional

SLASH = "/"

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
                "search": lambda keyword, surah = "all", translation = self.quran_translation: self.base_quran_url + "/search/" + keyword + SLASH + surah + SLASH + translation  
            },
            "bible": {
                "chapter": lambda book, chapter, translation = self.bible_translation: self.base_bible_url + SLASH + book + str(chapter) + f"?translation={translation}",
                "verse": lambda book, chapter, starting_verse, ending_verse = "", translation = self.bible_translation: self.base_bible_url + SLASH + book + str(chapter) + ":" + str(starting_verse) + ("-" + str(ending_verse) if str(ending_verse) else "") + f"?translation={translation}"
            }
        }
        self._session = requests.Session()

    def request(
        self,
        url: str,
        method: str = "get"
    ):
        try: 
            req = getattr(self._session, method.lower())
        except AttributeError:
            raise AttributeError(f"Cannot find method: {method}")

        url = url.replace(" ", "%20")
        print(url)
        res = req(url)
        status_code = res.status_code
        print(status_code)
        if not status_code == 200:
            data = res.json()
            match res.status_code:
                case 204:
                    return None
                    
                case 404:
                    try:
                        raise NotFound(data["data"])
                    except KeyError:
                        raise NotFound(data["error"])
                    except TypeError:
                        raise NotFound(data)

                case 429:
                    raise TooManyRequests()
        return res.json()

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
            return Quran(**res)

    def fetch_book_chapter(
        self, 
        chapter, 
        *, 
        book: str = "", 
        beginning_verse: Optional[int, str] = "",
        ending_verse: Optional[int, str] = "",
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
            res = self.request(url, "get")
            edition = res["data"]["edition"]
            for verse in res["data"]["ayahs"]:
                verse["translation"] = edition
            res["data"]["translation"] = edition
            return Surah(data=res)

    def fetch_chapter_verse(
        self, 
        book: str = "", 
        *,
        citation: str,
        translation: str = ""
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
                data = data[0]
                data["reference"] = res["reference"]
                data["translation"] = {
                    "name": res["translation_name"],
                    "id": res["translation_id"],
                    "note": res["translation_note"]
                }
                
                return BibleVerse(**data)

        else:
            url = self.urls["quran"]["verse"](citation, translation or self.quran_translation)
            data = self.request(url)
            edition = data["data"]["edition"]
            data["data"]["translation"] = edition
            data["data"]["surah"]["translation"] = edition
            return Ayah(data=data)

    def search(self, keyword: str, chapter: Optional[str, int] = "all", translation: str = ""):
        url = self.urls["quran"]["search"](keyword, chapter, translation or self.quran_translation)
        data = self.request(url)
        verses = data["data"]["matches"]
        for verse in verses:
            verse["translation"] = verse["edition"]
            verse["surah"]["translation"] = verse["edition"]
        return [Ayah(data=d) for d in verses]