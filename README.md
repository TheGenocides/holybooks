# hollybooks
Hollybooks is an api wrapper consist with 3 api(s). Right now (6/25/2021) it only have 1 api. 
 
# Installation 
```bash
No instalation for now!
```

# Usage

```python
import hollybooks

# To return a quran's verse/chapter(surah) and other info

surah=hollybooks.quran.Surah(1) #1 is the first chapter
print(surah.name('eng')) #Only support arabic(ar) and english(eng)
#return al-fatihah

print(surah.name_mean())
#return The Opener
```

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

# License
[MIT](https://choosealicense.com/licenses/mit/)
