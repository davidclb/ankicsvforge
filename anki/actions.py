import logging
from typing import Any

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
    "Arabic",
]

INORDERFIELDS_VOCAB = [
    "Transliteration",
    "Meaning",
    "Arabic",
    "Dual",
    "Feminine",
    "Plural",
    "Source",
]

SHARED_CSS = """
.card {
  font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: #F7F2E4;
  color: #354031;
  text-align: center;
  padding: 34px 22px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

/* front: the prompt (meaning, or verb+tense) */
.prompt {
  font-size: 22px;
  font-weight: 500;
  color: #354031;
}
.prompt .gloss { opacity: .6; }

/* tense label (conjugation) */
.tense {
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #6E8455;
  font-weight: 700;
  margin-top: 10px;
}

/* type-in field — Anki injects it, we style the input */
input[type=text] {
  font-family: inherit;
  font-size: 18px;
  text-align: center;
  color: #354031;
  background: #FDFBF4;
  border: 1.5px solid #C7CBB6;
  border-radius: 9px;
  padding: 8px 14px;
  margin-top: 14px;
}

/* vocab answer: transliteration then arabic */
.translit {
  font-size: 30px;
  font-weight: 700;
  color: #445A2C;
  letter-spacing: -0.01em;
}
.arabic {
  font-family: 'Noto Naskh Arabic', 'Traditional Arabic', 'Geeza Pro', serif;
  direction: rtl;
  font-size: 38px;
  font-weight: 600;
  color: #354031;
  margin-top: 4px;
}

/* divider */
hr, hr#answer {
  border: none;
  height: 1px;
  background: rgba(80,90,55,.16);
  width: 55%;
  margin: 16px auto;
}

/* secondary info (forms, variants) */
.forms {
  font-size: 15px;
  color: #8A9584;
  margin-top: 4px;
}

/* word origin (song, series...) */
.source {
  font-size: 12px;
  color: #A79B82;
  font-style: italic;
  margin-top: 10px;
}

/* conjugation table (back) */
.conj {
  background: #FDFBF4;
  border-radius: 12px;
  box-shadow: inset 0 0 0 1px rgba(80,90,55,.14);
  padding: 6px 16px;
  max-width: 420px;
  margin: 6px auto 0;
}
.conj-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: 7px 0;
  border-bottom: 1px solid rgba(80,90,55,.12);
}
.conj-row:last-child { border-bottom: none; }
.conj-pro { font-size: 13px; color: #8A9584; font-weight: 600; }
.conj-form { font-size: 18px; color: #445A2C; font-weight: 600; }
"""


def build_field_verb(verb: Verb) -> dict:
    return {
        "Verb": verb.verb,
        "Meaning": verb.meaning,
        "Tense": verb.tense,
        **{
            p.capitalize(): verb.conjugation.get(p.lower(), "").split(" / ")[0].strip()
            for p in PRONOUNS
        },
        "FormVariant": " | ".join(
            f"{p}: {v}" for p, v in verb.conjugation.items() if " / " in v
        ),
        "Arabic": verb.arabic,
    }


def build_field_vocab(vocab: Vocab) -> dict:
    return {
        "Transliteration": vocab.transliteration,
        "Meaning": vocab.meaning,
        "Arabic": vocab.arabic,
        "Dual": vocab.dual,
        "Feminine": vocab.feminine,
        "Plural": vocab.plural,
        "Source": vocab.source,
    }


def check_model(modelName: str) -> bool:
    models = invoke("modelNames")
    return modelName in models


def get_note_verb_id(verb: str, tense: str) -> int:
    params_findNotes = {"query": f'"Verb:{verb}" "Tense:{tense}"'}
    result = invoke("findNotes", **params_findNotes)
    return result


def get_note_vocab_id(transliteration: str) -> int:
    params_findNotes = {"query": f'"Transliteration:{transliteration}"'}
    result = invoke("findNotes", **params_findNotes)
    return result


def check_note_verb(verb: str, tense: str) -> bool:
    params_findNotes = {"query": f'"Verb:{verb}" "Tense:{tense}"'}
    result = invoke("findNotes", **params_findNotes)
    return result != []


def check_note_vocab(transliteration: str) -> bool:
    params_findNotes = {"query": f'"Transliteration:{transliteration}"'}
    result = invoke("findNotes", **params_findNotes)
    return result != []


def make_template(pronom: str) -> dict:
    return {
        "Name": f"Card {pronom}",
        "Front": f"""<div class="prompt">({{{{Meaning}}}})</div>
            <div class="tense">{pronom} — {{{{Tense}}}}</div>
            {{{{type:{pronom}}}}}""",
        "Back": f"""<div class="prompt">({{{{Meaning}}}})</div>
            <div class="tense">{pronom} — {{{{Tense}}}}</div>
            {{{{type:{pronom}}}}}
            <hr id="answer">
            <span class="translit">{{{{hint:Verb}}}}</span>
            {{{{#FormVariant}}}}
            <hr>
            <div class="forms">{{{{FormVariant}}}}</div>
            {{{{/FormVariant}}}}""",
    }


def create_model_verb(modelName: str):

    params = {
        "modelName": modelName,
        "inOrderFields": INORDERFIELDS_VERB,
        "css": SHARED_CSS,
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
        "css": SHARED_CSS,
        "isCloze": False,
        "cardTemplates": [
            {
                "Name": "Card VOCAB",
                "Front": '<div class="prompt">{{Meaning}}</div>',
                "Back": """<div class="prompt">{{Meaning}}</div>
                <hr>
                <div class="translit">{{Transliteration}}</div>
                {{#Arabic}}<div class="arabic">{{Arabic}}</div>{{/Arabic}}
                {{#Feminine}}<div class="forms">féminin : {{Feminine}}</div>{{/Feminine}}
                {{#Dual}}<div class="forms">duel : {{Dual}}</div>{{/Dual}}
                {{#Plural}}<div class="forms">pluriel : {{Plural}}</div>{{/Plural}}
                {{#Source}}<div class="source">{{Source}}</div>{{/Source}}""",
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
            "fields": build_field_verb(verb),
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
            "fields": build_field_vocab(vocab),
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


def updateNotefields(elem: Verb | Vocab):
    if isinstance(elem, Verb):
        if toUpdate(elem):
            note_id = get_note_verb_id(elem.verb, elem.tense)
            desired_state = build_field_verb(elem)
            params_updateNoteFields = {
                "note": {
                    "id": note_id,
                    "fields": desired_state,
                }
            }
            invoke("updateNoteFields", **params_updateNoteFields)
    if isinstance(elem, Vocab):
        if toUpdate(elem):
            note_id = get_note_vocab_id(elem.transliteration)
            desired_state = build_field_vocab(elem)
            params_updateNoteFields = {
                "note": {
                    "id": note_id,
                    "fields": desired_state,
                }
            }
            invoke("updateNoteFields", **params_updateNoteFields)


def toUpdate(elem: Verb | Vocab) -> bool:
    if isinstance(elem, Verb):
        note_id = get_note_verb_id(elem.verb, elem.tense)
        params_noteInfo = {"notes": note_id}
        result = invoke("notesInfo", **params_noteInfo)
        actual_state = result[0]["fields"]
        desired_state = build_field_verb(elem)
        if actual_state == desired_state:
            return False
        else:
            for field, desired_value in desired_state.items():
                actual_value = actual_state[field]["value"]
                if (
                    actual_value != desired_value
                ):  ## value level , not direct comparison between objects
                    return True
            return False
    elif isinstance(elem, Vocab):
        note_id = 0
        note_id = get_note_vocab_id(elem.transliteration)
        params_noteInfo = {"notes": note_id}
        result = invoke("notesInfo", **params_noteInfo)
        actual_state = result[0]["fields"]
        desired_state = build_field_vocab(elem)
        if actual_state == desired_state:
            return False
        else:
            for field, desired_value in desired_state.items():
                actual_value = actual_state[field]["value"]
                if (
                    actual_value != desired_value
                ):  ## value level , not direct comparison between objects
                    return True
            return False
