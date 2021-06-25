# hollybooks

An Api wrapper for extract info from 3 diffreant holly books. Right now (6/25/2021) it only have 1 api which connect to the quran api. My plan is to have 3 Api(s).

# Installation

```bash
No instalation for now!
```

# Usage

```python
import hollybooks

# To return a quran's verse/chapter(surah) and other info

surah=hollybooks.Surah.request(1) #1 is the first chapter
print(surah.name('eng')) #Only support arabic(ar) and english(eng)
#return al-fatihah


# To return a bible verse's info

bible_verses=hollybooks.Bible.request(
    "2 Corinthians", chapter=4,
    starting_verse=16, ending_verse=18
)  # this gets the info of 2 Corinthians 4:16-18

for verse in bible_verses.verses:
    print(
        verse.citation,  # The citation of the current verse
        verse  # executes the __str__ method of the BibleVerse class (it returns the verse itself)
    )
```

# API That I Used

[Qur'an](https://alquran.cloud/api)

[Bible](https://bible-api.com/)

Torah - Not available

# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

# License

[MIT](https://choosealicense.com/licenses/mit/)
