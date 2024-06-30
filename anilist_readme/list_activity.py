from datetime import datetime, tzinfo
from enum import auto, Enum
from dateutil import tz

from .config import EMOJI_DICT


class Language(Enum):
    romaji = auto()
    english = auto()
    native = auto()


def validate_language(lang: str) -> Language:
    """
    Check if the language is valid.
    """
    languages = [x.name for x in Language]
    if lang.lower() in languages:
        return Language[lang.lower()]
    raise ValueError(
        f"'{lang}'' is not a valid language. Must be: '{', '.join(languages)}'"
    )


class ListActivity:
    def __init__(
        self,
        activity_data: dict,
        timezone: str,
        preferred_lang: Language,
        date_format: str,
        text_format: str,
    ) -> None:
        self.type: str = activity_data["type"]
        self.created_at = custom_datetime_format(
            dt=datetime.fromtimestamp(activity_data["createdAt"], tz.gettz(timezone)),
            date_format=date_format,
        )
        self.text_format = text_format
        self.progress: str = activity_data["progress"]
        self.status: str = activity_data["status"]
        self.title: str = (
            activity_data["media"]["title"][
                preferred_lang.name if preferred_lang else "english"
            ]
            or activity_data["media"]["title"]["romaji"]
            or activity_data["media"]["title"]["native"]
        )
        self.url: str = activity_data["media"]["siteUrl"]

    def __str__(self) -> str:
        if self.text_format == "md":
            return f"-   {EMOJI_DICT[self.type]} {self.status.capitalize()} {f'{self.progress} of ' if self.progress else ''}[{self.title}]({self.url}) ({self.created_at})"
        else:
            return f"-   {EMOJI_DICT[self.type]} {self.status.capitalize()} {f'{self.progress} of ' if self.progress else ''}<a href='{self.url}'>{self.title}</a> ({self.created_at})<br>"

def custom_datetime_format(dt: datetime, date_format: str) -> str:
    new_format = (
        date_format.replace("{h}", "%H")
        .replace("{m}", "%M")
        .replace("{D}", "%d")
        .replace("{M}", "%m")
        .replace("{MW}", "%B")
        .replace("{Y}", "%Y")
    )

    return dt.strftime(new_format)
