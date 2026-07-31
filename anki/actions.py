import logging
from typing import Any

from anki.api import invoke
from models.models import Grammar, Sentence, Verb, Vocab

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

INORDERFIELDS_SENTENCE = [
    "Topic",
    "Order",
    "Type",
    "Transliteration",
    "Meaning",
    "Arabic",
    "Source",
]

INORDERFIELDS_GRAMMAR = [
    "Rule",
    "Explanation",
    "Example",
    "Arabic",
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

/* keep a readable column on wide screens */
.card > * { max-width: 640px; margin-left: auto; margin-right: auto; }

/* type badge for sentences (question / answer / text) */
.badge {
  display: inline-block;
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #6E8455;
  font-weight: 700;
  border: 1px solid rgba(110,132,85,.4);
  border-radius: 999px;
  padding: 3px 12px;
  margin-bottom: 14px;
}

/* sentence cards: long text, read comfortably (left-aligned, wider) */
.sentence {
  font-size: 20px;
  font-weight: 600;
  color: #445A2C;
  line-height: 1.6;
  text-align: left;
  max-width: 60ch;
}
.sentence-tr {
  font-size: 16px;
  color: #6B6459;
  line-height: 1.6;
  text-align: left;
  max-width: 60ch;
  margin-top: 6px;
}

/* grammar cards: rule + explanation + example */
.rule {
  font-size: 22px;
  font-weight: 700;
  color: #354031;
}
.explanation {
  font-size: 17px;
  color: #4A4A3A;
  line-height: 1.6;
  text-align: left;
  max-width: 60ch;
  margin-top: 4px;
}
.example {
  font-size: 15px;
  color: #445A2C;
  font-style: italic;
  background: #FDFBF4;
  border-left: 3px solid #6E8455;
  border-radius: 6px;
  padding: 10px 14px;
  text-align: left;
  max-width: 60ch;
  margin-top: 12px;
}

/* responsive: shrink arabic on small screens (AnkiDroid) */
@media (max-width: 420px) {
  .arabic { font-size: 30px; }
  .translit { font-size: 26px; }
  .prompt, .rule { font-size: 20px; }
}
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


def build_field_sentence(sentence: Sentence) -> dict:
    return {
        "Topic": sentence.topic,
        "Order": sentence.order,
        "Type": sentence.type,
        "Transliteration": sentence.transliteration,
        "Meaning": sentence.meaning,
        "Arabic": sentence.arabic,
        "Source": sentence.source,
    }


def build_field_grammar(grammar: Grammar) -> dict:
    return {
        "Rule": grammar.rule,
        "Explanation": grammar.explanation,
        "Example": grammar.example,
        "Arabic": grammar.arabic,
        "Source": grammar.source,
    }


def check_model(modelName: str) -> bool:
    models = invoke("modelNames")
    return modelName in models


def natural_key_query(note: Verb | Vocab | Sentence | Grammar) -> str:
    if isinstance(note, Verb):
        return f'"Verb:{note.verb}" "Tense:{note.tense}"'
    if isinstance(note, Vocab):
        return f'"Transliteration:{note.transliteration}"'
    if isinstance(note, Sentence):
        return f'"Topic:{note.topic}" "Order:{note.order}"'
    if isinstance(note, Grammar):
        return f'"Rule:{note.rule}"'
    raise ValueError(f"Unknown note type: {type(note)}")


def get_note_id(note: Verb | Vocab | Sentence | Grammar) -> list[int]:
    result = invoke("findNotes", query=natural_key_query(note))
    return result


def check_note(note: Verb | Vocab | Sentence | Grammar) -> bool:
    """True if a note with this natural key already exists."""
    return get_note_id(note) != []


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


def create_model_sentence(modelName: str):
    params = {
        "modelName": modelName,
        "inOrderFields": INORDERFIELDS_SENTENCE,
        "css": SHARED_CSS,
        "isCloze": False,
        "cardTemplates": [
            {
                "Name": "Card SENTENCE",
                "Front": """{{#Type}}<div class="badge">{{Type}}</div>{{/Type}}
<div class="sentence-tr">{{Meaning}}</div>""",
                "Back": """{{#Type}}<div class="badge">{{Type}}</div>{{/Type}}
<div class="sentence-tr">{{Meaning}}</div>
<hr>
<div class="sentence">{{Transliteration}}</div>
{{#Arabic}}<div class="arabic">{{Arabic}}</div>{{/Arabic}}
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


def create_model_grammar(modelName: str):
    params = {
        "modelName": modelName,
        "inOrderFields": INORDERFIELDS_GRAMMAR,
        "css": SHARED_CSS,
        "isCloze": False,
        "cardTemplates": [
            {
                "Name": "Card GRAMMAR",
                "Front": '<div class="rule">{{Rule}}</div>',
                "Back": """<div class="rule">{{Rule}}</div>
<hr>
<div class="explanation">{{Explanation}}</div>
{{#Example}}<div class="example">{{Example}}</div>{{/Example}}
{{#Arabic}}<div class="arabic">{{Arabic}}</div>{{/Arabic}}
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
    if check_note(verb):
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
    if check_note(vocab):
        logging.info(f"Note for {vocab.transliteration} already exist")
        return False

    else:
        logging.info(f"Creation of note for {vocab.transliteration} ")
        invoke("addNote", **params_addNote)
        return True


def add_notes_sentence(sentence: Sentence, deckName: str, modelName: str) -> bool:
    params_addNote = {
        "note": {
            "deckName": deckName,
            "modelName": modelName,
            "fields": build_field_sentence(sentence),
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": "Default",
                    "checkChildren": False,
                    "checkAllModels": False,
                },
            },
            "tags": ["type::sentence"],
        }
    }
    # verifier d'abord que la note existe ou pas
    if check_note(sentence):
        logging.info(f"Note for {sentence.topic} - {sentence.order} already exist")
        return False

    else:
        logging.info(f"Creation of note for {sentence.topic} - {sentence.order} ")
        invoke("addNote", **params_addNote)
        return True


def add_notes_grammar(grammar: Grammar, deckName: str, modelName: str) -> bool:
    params_addNote = {
        "note": {
            "deckName": deckName,
            "modelName": modelName,
            "fields": build_field_grammar(grammar),
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": "Default",
                    "checkChildren": False,
                    "checkAllModels": False,
                },
            },
            "tags": ["type::grammar"],
        }
    }
    # verifier d'abord que la note existe ou pas
    if check_note(grammar):
        logging.info(f"Note for {grammar.rule} already exist")
        return False

    else:
        logging.info(f"Creation of note for {grammar.rule}")
        invoke("addNote", **params_addNote)
        return True


def build_fields(elem: Verb | Vocab | Sentence | Grammar) -> dict:
    """Dispatch to the right build_field_* according to the note type."""
    if isinstance(elem, Verb):
        return build_field_verb(elem)
    if isinstance(elem, Vocab):
        return build_field_vocab(elem)
    if isinstance(elem, Sentence):
        return build_field_sentence(elem)
    if isinstance(elem, Grammar):
        return build_field_grammar(elem)
    raise ValueError(f"Unknown note type: {type(elem)}")


def toUpdate(elem: Verb | Vocab | Sentence | Grammar) -> bool:
    """True if the existing note differs from the desired (CSV) state."""
    note_id = get_note_id(elem)
    if not note_id:
        return False  # no existing note -> not an update (it's a create)
    result = invoke("notesInfo", notes=note_id)
    actual_state = result[0]["fields"]
    desired_state = build_fields(elem)
    for field, desired_value in desired_state.items():
        actual_value = actual_state[field][
            "value"
        ]  # value level, not object comparison
        if actual_value != desired_value:
            return True
    return False


def updateNotefields(elem: Verb | Vocab | Sentence | Grammar):
    """Update an existing note in place (preserves SRS) if its content changed."""
    if toUpdate(elem):
        note_id = get_note_id(elem)
        params_updateNoteFields = {
            "note": {
                "id": note_id[0],
                "fields": build_fields(elem),
            }
        }
        invoke("updateNoteFields", **params_updateNoteFields)
