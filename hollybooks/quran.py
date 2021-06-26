from typing import Union, Optional

__all__ = ("Surah", "Ayah", "Search")

class ApiError(Exception):
    def __init__(self, status: int, msg: str) -> None:
        super().__init__(f"Api has an error, return code: {status}.\n{msg}")
	
class ContentTypeError(Exception):
    def __init__(self, class_:str, mode:str, first_query: Optional[Union[str, int]], second_query: Optional[Union[str, int]]) -> None:
        super().__init__(f"Attempt to decode JSON with unexpected mimetype: Return code: None\nlink: http://api.alquran.cloud/v1/{mode}/{first_query}:{second_query}/en.asad" if class_ == "Ayah" else f"Attempt to decode JSON with unexpected mimetype: Return code: None\nlink: http://api.alquran.cloud/v1/{mode}/{first_query}/{second_query}/en.asad")

class NumberError(Exception):
    def __init__(self, mode:int, obj:str, first_query: int, second_query: Optional[Union[str, int]]) -> None:
        super().__init__(f"{obj} must above {first_query}" if mode == 0 else f"{obj} must be between {first_query} to {second_query}")


class WrongLang(Exception):
    def __init__(self, lang:str) -> None:
        super().__init__(f"The lang '{lang}' is not supported, it only support arabic(ar) and english(eng)")


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
				code=self.request['code'], msg=self.request['data']
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
				code=self.request['code'], msg=self.request['data']
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
            raise WrongLang(lang=lang)

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
        ayah: int = 1, *,
        text: bool = True,
        number_in_quran: bool = True,
		number_in_surah: bool = True,
        juz: bool = True,
        manzil: bool = True,
		page: bool = True,
		ruku: bool = True,
		hizbquarter: bool = True,
		sajda : bool = True
    ):
        if ayah <= 0:
            raise NumberError(mode=0, obj="ayah", first_query=1, second_query=None)

        elif ayah > int(Surah.request(self.surah).number_ayahs):
            raise NumberError(mode=1, obj="ayah", first_query=1, second_query=Surah.request(self.surah).number_ayahs)

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
				"page": self.ayah[ayah]["page"] if text else None,
                "ruku": self.ayah[ayah]["ruku"]
                if number_in_quran
                else None,
                "hizbquarter": self.ayah[ayah]["hizbQuarter"]
                if number_in_surah
                else None,
                "sajda": self.ayah[ayah]["sajda"] if juz else None
            }
            return data

class Ayah:
	def __init__(self, surah:int=None, *, ayah:int=None):
		self.surah = surah
		self.ayah = ayah

	@classmethod
	def request(
		cls, 
		surah:int=None, *, 
		ayah:int=None,
		loop=None
	):
		try:
			import requests
		except ImportError:
			raise ImportError(
		"Please Install the requests module if you want to make a sync request."
		)

		self = cls(surah, ayah=ayah)
		self.request = requests.get(
		f"http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/en.asad"
		).json()
		self.data = self.request["data"]
		if self.request["code"] > 202:
			raise ApiError(
				code=self.request['code'], msg=self.request['data']
			)
		return self

	@classmethod
	async def async_request(
		cls, 
		surah:int=None, *, 
		ayah:int=None,
		loop=None
	):
		try:
			import aiohttp
		except ImportError:
			raise ImportError(
				"Please Install the aiohttp module if you want to make an async request."
			)

		self = cls(surah, ayah=ayah)

		try:
			async with aiohttp.ClientSession(loop=loop) as session:
				async with session.get(
					f"http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/en.asad"
				) as resp:
					self.request = await resp.json()
		except aiohttp.client_exceptions.ContentTypeError:
			raise ContentTypeError(class_="Ayah", mode='ayah', first_query=surah, second_query=surah)
		
		self.data = self.request["data"]
		if self.request["code"] > 202:
			raise ApiError(
				code=self.request['code'], msg=self.request['data']
			)
		return self

	@property
	def api_code(self):
		return self.request['code']

	@property
	def api_status(self):
		return self.request['status']

class Search:
	def __init__(self, mention:str=None, *, surah:Optional[Union[str, int]]=None, request: int=None):
		self.mention = mention
		self.surah = surah
		self.req = request
	
	@classmethod
	async def async_request(
		cls, 
		mention:str=None, *, 
		surah:Optional[Union[str, int]]=None,
		request:int=None,
		loop=None
	):
		try:
			import aiohttp
		except ImportError:
			raise ImportError(
				"Please Install the aiohttp module if you want to make an async request."
			)


		self = cls(mention, surah=surah, request=request)

		try:
			async with aiohttp.ClientSession(loop=loop) as session:
				async with session.get(
					f"http://api.alquran.cloud/v1/search/{mention}/{surah}/en.pickthall"
				) as resp:
					self.request = await resp.json()
		except aiohttp.client_exceptions.ContentTypeError:
			raise ContentTypeError(class_="Search", mode='search', first_query=mention, second_query=surah)
		
		self.data = self.request["data"]
		self.matches = self.data['matches']
		if self.request["code"] > 202:
			raise ApiError(
				code=self.request['code'], msg=self.request['data']
			)

		return self

	@classmethod
	def request(
		cls, 
		mention: str=None, *, 
		surah: Optional[Union[str, int]]=None,
		request: int = None
	):
		try:
			import requests
		except ImportError:
			raise ImportError(
		"Please Install the requests module if you want to make a sync request."
		)

		self = cls(mention, surah=surah, request=request)
		self.request = requests.get(
		f"http://api.alquran.cloud/v1/search/{mention}/{surah}/en.pickthall"
		).json()
		self.data = self.request["data"]
		self.matches = self.data['matches']
		if self.request["code"] > 202:
			raise ApiError(
				code=self.request['code'], msg=self.request['data']
			)
		return self
		
	@property
	def count(self):
		return self.data['count']

	@property
	def api_code(self):
		return self.request['code']

	@property
	def api_status(self):
		return self.request['status']

	def find(self):
		data=[]
		if self.req == None:
			for num in range(self.data['count']):
				data.append(self.matches[num]['text'])
			return data

		else:	
			for num in range(self.req):
				data.append(self.matches[num]['text'])
			return data