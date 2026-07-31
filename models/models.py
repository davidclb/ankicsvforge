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


@dataclass
class Sentence:
    topic: str
    order: str
    type: str
    transliteration: str
    meaning: str
    arabic: str
    source: str


@dataclass
class Grammar:
    rule: str
    explanation: str
    example: str
    arabic: str
    source: str
