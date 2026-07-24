import logging

from anki.api import invoke
from models.models import Verb, Vocab

PRONOUNS = ["Ana", "Enta", "Ente", "Houwe", "Hiye", "Nehna", "Ento", "Henne"]
INORDERFIELDS_VERB = [
    "Verb",
    "Meaning",
    "Tense",
    "Ana",
    "Enta",
    "Ente",
    "Houwe",
    "Hiye",
    "Nehna",
    "Ento",
    "Henne",
    "FormVariant",
    "Arab",
]

INORDERFIELDS_VOCAB = [
    "Transliteration",
    "Meaning",
    "Arab",
]


def check_model(modelName: str) -> bool:
    models = invoke("modelNames")
    return modelName in models


def check_note_verb(verb: str, tense: str) -> bool:
    params_findNotes = {"query": f"Verb:{verb} Tense:{tense}"}
    result = invoke("findNotes", **params_findNotes)
    return result != []


def check_note_vocab(transliteration: str) -> bool:
    params_findNotes = {"query": f"Transliteration:{transliteration}"}
    result = invoke("findNotes", **params_findNotes)
    return result != []


def make_template(pronom: str) -> dict:
    return {
        "Name": f"Card {pronom}",
        "Front": f"""({{{{Meaning}}}})
                     <br><br>
                      {pronom}— {{{{Tense}}}}
                    <br><br>
                    {{{{type:{pronom}}}}}""",
        "Back": f"""{{{{FrontSide}}}}
                    <hr id="answer">
                    {{{{hint:Verb}}}} 
                    {{{{#FormVariant}}}}
                    <hr>
                    {{{{FormVariant}}}}
                    {{{{/FormVariant}}}}""",
    }


def create_model_verb(modelName: str):

    params = {
        "modelName": modelName,
        "inOrderFields": INORDERFIELDS_VERB,
        "css": "Optional CSS with default to builtin css",
        "isCloze": False,
        "cardTemplates": [make_template(p) for p in PRONOUNS],
    }
    if check_model(modelName):
        logging.info(f"{modelName} model already exist")

    else:
        logging.info(f"{modelName} model doesn't exist")
        logging.info("Creating...")
        invoke("createModel", **params)


def create_model_vocab(modelName: str):

    params = {
        "modelName": modelName,
        "inOrderFields": INORDERFIELDS_VOCAB,
        "css": "Optional CSS with default to builtin css",
        "isCloze": False,
        "cardTemplates": [
            {
                "Name": f"Card VOCAB",
                "Front": f"""({{{{Meaning}}}})
                     <br><br>""",
                "Back": f"""
                    {{{{Transliteration}}}}
                    <hr>
                    {{{{Arab}}}}""",
            }
        ],
    }
    if check_model(modelName):
        logging.info(f"{modelName} model already exist")

    else:
        logging.info(f"{modelName} model doesn't exist")
        logging.info("Creating...")
        invoke("createModel", **params)


def check_deck(deckName: str) -> bool:
    decks = invoke("deckNames")
    return deckName in decks


def create_deck(deckName: str):
    if check_deck(deckName):
        logging.info(f"{deckName} deck already exist")

    else:
        logging.info(f"{deckName} deck doesn't exist")
        logging.info("Creating...")
        invoke("createDeck", deck=deckName)
        logging.info("Deck created")


def add_notes_verb(verb: Verb, deckName: str, modelName: str) -> bool:
    params_addNote = {
        "note": {
            "deckName": deckName,
            "modelName": modelName,
            "fields": {
                "Verb": verb.verb,
                "Meaning": verb.meaning,
                "Tense": verb.tense,
                **{
                    p.capitalize(): verb.conjugation.get(p.lower(), "")
                    .split(" / ")[0]
                    .strip()
                    for p in PRONOUNS
                },
                "FormVariant": " | ".join(
                    f"{p}: {v}" for p, v in verb.conjugation.items() if " / " in v
                ),
                "Arab": verb.arab,
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": "Default",
                    "checkChildren": False,
                    "checkAllModels": False,
                },
            },
            "tags": ["type::verb", f"verb::tense::{verb.tense}"],
        }
    }
    # verifier d'abord que la note existe ou pas
    if check_note_verb(verb.verb, verb.tense):
        logging.info(f"Note for {verb.verb} {verb.tense} already exist")
        return False
    else:
        logging.info(f"Creation of note for {verb.verb} {verb.tense} ")
        invoke("addNote", **params_addNote)
        return True
    # ensuite montrer toute les cartes qui vont etre crées


def add_notes_vocab(vocab: Vocab, deckName: str, modelName: str) -> bool:
    params_addNote = {
        "note": {
            "deckName": deckName,
            "modelName": modelName,
            "fields": {
                "Transliteration": vocab.transliteration,
                "Meaning": vocab.meaning,
                "Arab": vocab.arab,
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": "Default",
                    "checkChildren": False,
                    "checkAllModels": False,
                },
            },
            "tags": ["type::vocab"],
        }
    }
    # verifier d'abord que la note existe ou pas
    if check_note_vocab(vocab.transliteration):
        logging.info(f"Note for {vocab.transliteration} already exist")
        return False

    else:
        logging.info(f"Creation of note for {vocab.transliteration} ")
        invoke("addNote", **params_addNote)
        return True
