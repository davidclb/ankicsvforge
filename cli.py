import argparse
from pathlib import Path
import logging
from anki.actions import (
    add_notes_verb,
    add_notes_vocab,
    check_note_verb,
    check_note_vocab,
    create_deck,
    create_model_verb,
    create_model_vocab,
    toUpdate,
)

from models.models import Verb, Vocab
from parsing.parser_verb import parse_verb
import sys

from parsing.parser_vocab import parse_vocab

DECK_NAME_VERB = "LebaneseConjugator"
MODEL_NAME_VERB = "LebaneseConjugator"
MODEL_NAME_VOCAB = "LebaneseVocab"
DECK_NAME_VOCAB = "LebaneseVocab"


def label_run_error(note: Verb | Vocab) -> str:
    if isinstance(note, Verb):
        return f"{note.verb} / {note.tense}"
    else:
        return note.transliteration


def label_dryrun(note: Verb | Vocab, operation: str) -> str:
    if operation == "create":
        if isinstance(note, Verb):
            return f"CREATE {note.verb} / {note.tense}"
        elif isinstance(note, Vocab):
            return f"CREATE {note.transliteration} / {note.meaning}"
    if operation == "update":
        if isinstance(note, Verb):
            return f"UPDATE {note.verb} / {note.tense}"
        elif isinstance(note, Vocab):
            return f"UPDATE {note.transliteration} / {note.meaning}"


def run_import(notes, add_fn, deck, model, label_fn):
    errors = []
    nb_created = 0
    nb_skipped = 0

    for note in notes:
        try:
            created = add_fn(note, deck, model)
            if created:
                nb_created += 1
            else:
                nb_skipped += 1

        except Exception as e:
            logging.error(f"couldn't create note for {label_fn(note)}")
            errors.append(note)
    logging.info(f"{nb_created} notes  created")
    logging.info(f"{nb_skipped} notes  skipped")

    logging.info(f"{len(errors)} errors")
    for error in errors:
        logging.info(f"couldn't create note for {label_fn(error)}")


def run_dryrun(notes, label_fn):
    to_create = 0
    no_op = 0
    to_update = 0

    for note in notes:
        if isinstance(note, Verb):
            if not check_note_verb(note.verb, note.tense):
                to_create += 1
                logging.info(f"{label_fn(note,"create")}")
            else:
                no_op += 1
            if toUpdate(note):
                ###TODO: Add all the changes that will be applied in the dryrun ,
                ###Return gives a list of all the field that will changes the initial and the desired value
                to_update += 1
                logging.info(f"{label_fn(note,"update")}")

        if isinstance(note, Vocab):
            if not check_note_vocab(note.transliteration):
                to_create += 1
                logging.info(f"{label_fn(note,"create")}")
            else:
                no_op += 1
            if toUpdate(note):
                to_update += 1
                logging.info(f"{label_fn(note,"update")}")

    logging.info(f"Summary: {to_create} create, {no_op} no-op, {to_update} to update")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "type", type=str, help="type of notes", choices=["verb", "vocab", "sentence"]
    )
    parser.add_argument("csv", type=str, help="the csv file")
    parser.add_argument("--apply", help="create cards", action="store_true")
    args = parser.parse_args()

    target_file = Path(args.csv)
    if not target_file.exists():
        print("The target file doesn't exist")
        raise SystemExit(1)

    # choisir les bons "outils" selon le type — UNE seule fois
    if args.type == "verb":
        notes = parse_verb(args.csv)
        add_fn = add_notes_verb
        create_model_fn = create_model_verb
        deck = DECK_NAME_VERB
        model = MODEL_NAME_VERB
    elif args.type == "vocab":
        notes = parse_vocab(args.csv)
        add_fn = add_notes_vocab
        create_model_fn = create_model_vocab
        deck = DECK_NAME_VOCAB
        model = MODEL_NAME_VOCAB

    run_dryrun(notes, label_dryrun)

    if args.apply:
        reponse = input("Apply these changes? [y/N] ").strip().lower()
        if reponse in ("y", "yes", "o", "oui"):
            create_model_fn(model)
            create_deck(deck)
            run_import(notes, add_fn, deck, model, label_run_error)
