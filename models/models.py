from dataclasses import dataclass


@dataclass
class Verb:
    verb: str
    meaning: str
    tense: str
    conjugation: dict[str, str]
    arabic: str
    source: str


@dataclass
class Vocab:
    transliteration: str
    meaning: str
    arabic: str
    dual: str
    feminine: str
    plural: str
    source: str
