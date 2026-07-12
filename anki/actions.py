import logging

from anki.api import invoke
from models.verb import Verb

PRONOUNS = ["Ana", "Enta", "Ente", "Houwe", "Hiye", "Nehna", "Ento", "Henne"]
INORDERFIELDS = [
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


def check_model(modelName: str) -> bool:
    models = invoke("modelNames")
    return modelName in models


def make_template(pronom: str) -> dict:
    return {
        "Name": f"Card {pronom}",
        "Front": f"""({{{{Meaning}}}})
                     <br><br>
                      {pronom} — {{{{Tense}}}}
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


def create_conjugation_model():

    params = {
        "modelName": "LebaneseConjugator",
        "inOrderFields": INORDERFIELDS,
        "css": "Optional CSS with default to builtin css",
        "isCloze": False,
        "cardTemplates": [make_template(p) for p in PRONOUNS],
    }
    if not check_model("LebaneseConjugator"):
        logging.info("Lebanese conjugator model doesn't exist")
        logging.info("Creating...")
        invoke("createModel", **params)


def check_deck(deckName: str) -> bool:
    decks = invoke("deckNames")
    return deckName in decks


def create_conjugation_deck():
    if not check_deck("LebaneseConjugator"):
        logging.info("Lebanese conjugator deck doesn't exist")
        logging.info("Creating...")
        invoke("createDeck", deck="LebaneseConjugator")
        logging.info("Deck created")


def add_notes(verb: Verb):
    params = {
        "note": {
            "deckName": "LebaneseConjugator",
            "modelName": "LebaneseConjugator",
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
            "tags": ["type::verb ", f"verb::tense::{verb.tense}"],
        }
    }
    logging.debug("Les params")
    logging.debug(params)
    # verifier d'abord que la note existe ou pas
    # ensuite montrer toute les cartes qui vont etre crées
    invoke("addNote", **params)
