class ApiError(Exception):
    pass


class NumberError(Exception):
    pass


class WrongLang(Exception):
    pass


class Surah:
    def __init__(self, surah: int = None):
        self.surah = surah

    @classmethod
    def request(cls, surah: int = None):
        try:
            import requests
        except ImportError:
            raise ImportError(
                "Please Install the requests module if you want to make a sync request."
            )

        self = cls(surah)

        self.request = requests.get(
            f"https://api.alquran.cloud/v1/surah/{surah}/en.asad"
        ).json()
        self.data = self.request["data"]
        self.ayah = self.data["ayahs"]
        if self.request["code"] > 202:
            raise ApiError(
                f"Api has an error, return code: {self.request['code']}.\n{self.request['data']}"
            )

        return self

    @classmethod
    async def async_request(cls, surah: int = None, *, loop=None):
        try:
            import aiohttp
        except ImportError:
            raise ImportError(
                "Please Install the aiohttp module if you want to make an async request."
            )

        self = cls(surah)
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.get(
                f"https://api.alquran.cloud/v1/surah/{surah}/en.asad"
            ) as resp:
                self.request = await resp.json()
        self.data = self.request["data"]
        self.ayah = self.data["ayahs"]
        if self.request["code"] > 202:
            raise ApiError(
                f"Api has an error, return code: {self.request['code']}.\n{self.request['data']}"
            )

        return self

    @property
    def api_code(self):
        return self.request["code"]

    @property
    def api_status(self):
        return self.request["status"]

    def name(self, lang: str = "ar"):
        if lang == "ar" or lang.lower() == "arabic":
            return self.data["name"]

        elif lang == "eng" or lang.lower() == "english":
            return self.data["englishName"]

        else:
            error = f"The lang '{lang}' is not supported, it only support arabic and english"
            raise WrongLang(error)

    @property
    def name_mean(self):
        return self.data["englishNameTranslation"]

    @property
    def revelation_type(self):
        return self.data["revelationType"]

    @property
    def number_ayahs(self):
        return self.data["numberOfAyahs"]

    @property
    async def request_ayahs(self):
        data = []
        for number in range(Surah(self.surah).number_ayahs()):
            data.append(f"{self.ayah[number]['text']}")
        return data

    async def ayah_info(
        self,
        ayah: int = 1,
        *,
        text: bool = True,
        number_in_quran: bool = True,
        number_in_surah: bool = True,
        juz: bool = True,
        manzil: bool = True,
    ):
        if ayah <= 0:
            error = "Ayah must above the 0"
            raise NumberError(error)

        elif ayah > int(Surah(self.surah).number_ayahs()):
            error = f"Ayah must be between 1 to {Surah(self.surah).number_ayahs()}"
            raise NumberError(error)

        else:
            ayah -= 1
            data = {
                "text": self.ayah[ayah]["text"] if text else None,
                "number in quran": self.ayah[ayah]["number"]
                if number_in_quran
                else None,
                "number in surah": self.ayah[ayah]["numberInSurah"]
                if number_in_surah
                else None,
                "juz": self.ayah[ayah]["juz"] if juz else None,
                "manzil": self.ayah[ayah]["manzil"] if manzil else None,
            }
            return data
