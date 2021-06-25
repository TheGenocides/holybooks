import requests

class ApiError(Exception):
	pass 

class NumberError(Exception):
	pass

class WrongLang(Exception):
	pass

class Surah:
	def __init__(self, surah:int=None):
		self.surah = surah
		self.request = requests.get(f"https://api.alquran.cloud/v1/surah/{surah}/en.asad").json()
		self.data = self.request['data']
		self.ayah = self.data['ayahs']
		if self.request['code'] > 202:
			raise ApiError(f"Api has an error, return code: {self.request['code']}.\n{self.request['data']}")


	def api_code(self):
		return self.request["code"]

	def api_status(self):
		return self.request["status"]

	def name(self, lang:str='ar'):
		if lang == 'ar' or lang.lower() == 'arabic':
			return self.data['name']

		elif lang == 'eng' or lang.lower() == 'english':
			return self.data['englishName']

		else:
			error=f"The lang '{lang}' is not supported, it only support arabic and english"
			raise WrongLang(error)

	def name_mean(self):
		return self.data['englishNameTranslation']

	def revelation_type(self):
		return self.data['revelationType']

	def number_ayahs(self): 
		return self.data['numberOfAyahs']

	async def request_ayahs(self):
		data=[]
		for number in range(Surah(self.surah).number_ayahs()):
			data.append(f"{self.ayah[number]['text']}")
		return data

	async def ayah_info(self, ayah:int=1, text:bool=True, number_in_quran:bool=True, number_in_surah:bool=True, juz:bool=True, manzil:bool=True, ):		
		if ayah <= 0:
			error="Ayah must above the 0"
			raise NumberError(error)

		elif ayah > int(Surah(self.surah).number_ayahs()):
			error=f"Ayah must be between 1 to {Surah(self.surah).number_ayahs()}"
			raise NumberError(error)

		else:
			ayah -= 1
			data={'text': self.ayah[ayah]["text"] if text is True else None,
				'number in quran': self.ayah[ayah]["number"] if number_in_quran is True else None, 
				'number in surah': self.ayah[ayah]["numberInSurah"] if number_in_surah is True else None, 
				'juz': self.ayah[ayah]["juz"] if juz is True else None, 
				'manzil': self.ayah[ayah]["manzil"] if manzil is True else None}
			return data