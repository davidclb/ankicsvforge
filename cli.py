import argparse
from pathlib import Path
import logging
from anki.actions import (
    add_notes_verb,
    add_notes_vocab,
    create_deck,
    create_model_verb,
    create_model_vocab,
)

from models.models import Verb, Vocab
from parsing.parser_verb import parse_verb
import sys

from parsing.parser_vocab import parse_vocab

DECK_NAME_VERB = "LebaneseConjugator"
MODEL_NAME_VERB = "LebaneseConjugator"
MODEL_NAME_VOCAB = "LebaneseVocab"
DECK_NAME_VOCAB = "LebaneseVocab"


def label_error(note: Verb | Vocab) -> str:
    if isinstance(note, Verb):
        return f"{note.verb} / {note.tense}"
    else:
        return note.transliteration


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "type", type=str, help="type of notes", choices=["verb", "vocab", "sentence"]
    )
    parser.add_argument("csv", type=str, help="the csv file")
    parser.add_argument("--dry-run", help="preview cards that will be added")
    parser.add_argument("--apply", help="create cards")
    args = parser.parse_args()

    target_file = Path(args.csv)
    if not target_file.exists():
        print("The target file doesn't exist")
        raise SystemExit(1)

    if args.type == "verb":
        try:
            filepath_verb = args.csv
            verbs = parse_verb(filepath_verb)
        except FileNotFoundError:
            logging.error(f"Could not open file: {filepath_verb}")
            sys.exit(1)
        create_model_verb(MODEL_NAME_VERB)
        create_deck(DECK_NAME_VERB)
        run_import(
            verbs,
            add_notes_verb,
            DECK_NAME_VERB,
            MODEL_NAME_VERB,
            label_error,
        )

    if args.type == "vocab":
        try:
            filepath_vocab = args.csv
            vocabs = parse_vocab(filepath_vocab)
        except FileNotFoundError:
            logging.error(f"Could not open file: {filepath_vocab}")
            sys.exit(1)
        create_model_vocab(MODEL_NAME_VOCAB)
        create_deck(DECK_NAME_VOCAB)
        run_import(
            vocabs,
            add_notes_vocab,
            DECK_NAME_VOCAB,
            MODEL_NAME_VOCAB,
            label_error,
        )
