from .mixins import Translation

class QuranTranslation(Translation):
    def __init__(self, *args, **kwargs):
        self.language = kwargs.pop("language", None)
        self.author = kwargs.pop("englishName", None)
        self.format = kwargs.pop("format", None)
        self.type = kwargs.pop("type", None)
        self.direction = kwargs.pop("direction", None)
        super().__init__(**{
            "name": kwargs.pop("name"),
            "id": kwargs.pop("identifier"),
        })

class BibleTranslation(Translation):
    def __init__(self, *args, **kwargs):
        self.note = kwargs.pop("note")
        super().__init__(*args, **kwargs)