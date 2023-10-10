# holybooks

An API Wrapper for extracting info from the Al-Quran API and the Bible api. I will add more functions for certain api in the future! Documentation for this project is not avalaible at the moment. Full function can be seen in [client.py](https://github.com/TheGenocides/holybooks/blob/main/holybooks/client.py)

## Installation

Find the module [here](https://pypi.org/project/holybooks/).

```bash
pip install holybooks
```

## Usage

```python
# First make the client instance
from holybooks import Client

client = Client(
    quran_translation="en.asad",
    bible_translation="kjv"
)

client.fetch_ayah("2:255", "en.pickthall") #Retrives a verse from the Quran api. This will get chapter 2, verse 255. The second argument is the translation, if None specified the default translation is your quran_translation in your client instance.

client.fetch_verse("Genesis", "1:10", "kjv") #Retrives verses from the Bible API. This will get Genesis chapter 1, verse 1-10. The second argument is the translation, if None specified the default translation is your bible_translation in your client instance. 
```

## API's That I Used

[Qur'an](https://alquran.cloud/api)

[Bible](https://bible-api.com/)

## Contributing

Pull requests are welcome! Particularly for supporting other api(s).
Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)