from dataclasses import dataclass


@dataclass
class Verb:
    verb: str
    meaning: str
    tense: str
    conjugation: dict[str, str]
    arab: str


@dataclass
class Vocab:
    transliteration: str
    meaning: str
    arab: str
