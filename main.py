import logging
from anki.actions import (
    add_notes_verb,
    add_notes_vocab,
    create_deck,
    create_model_verb,
    create_model_vocab,
)
from parsing.parser_verb import parse_verb
import sys
from urllib.error import URLError

from anki.api import invoke
from parsing.parser_vocab import parse_vocab

DECK_NAME_VERB = "LebaneseConjugator"
MODEL_NAME_VERB = "LebaneseConjugator"
MODEL_NAME_VOCAB = "PiaVERB"
DECK_NAME_VOCAB = "PiaLebaneseVocab"


def main():
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    try:
        invoke("sync")
    except URLError:
        logging.error("Anki not open, please open first anki")
        sys.exit(1)

    try:
        filepath_verb = "example_verbes.csv"
        verbs = parse_verb(filepath_verb)
    except FileNotFoundError:
        logging.error(f"Could not open file: {filepath_verb}")
        sys.exit(1)
    create_model_verb(MODEL_NAME_VERB)
    create_deck(DECK_NAME_VERB)
    errors = []
    nb_created = 0
    nb_skipped = 0

    for verb in verbs:
        try:
            created = add_notes_verb(verb, DECK_NAME_VERB, MODEL_NAME_VERB)
            if created:
                nb_created += 1
            else:
                nb_skipped += 1

        except Exception as e:
            logging.error(f"couldn't create note for {verb.verb} / {verb.tense}")
            errors.append(verb)
    logging.info(f"{nb_created} notes  created")
    logging.info(f"{nb_skipped} notes  skipped")

    logging.info(f"{len(errors)} errors")
    for error in errors:
        logging.info(f"couldn't create note for {error.verb} {error.tense}")

    try:
        filepath_vocab = "example_vocab.csv"
        vocabs = parse_vocab(filepath_vocab)
    except FileNotFoundError:
        logging.error(f"Could not open file: {filepath_vocab}")
        sys.exit(1)
    create_model_vocab(MODEL_NAME_VOCAB)
    create_deck(DECK_NAME_VOCAB)
    errors = []
    nb_created = 0
    nb_skipped = 0

    for vocab in vocabs:
        try:
            created = add_notes_vocab(vocab, DECK_NAME_VOCAB, MODEL_NAME_VOCAB)
            if created:
                nb_created += 1
            else:
                nb_skipped += 1

        except Exception as e:
            logging.error(f"couldn't create note for {vocab.transliteration}")
            errors.append(vocab)
    logging.info(f"{nb_created} notes  created")
    logging.info(f"{nb_skipped} notes  skipped")
    logging.info(f"{len(errors)} errors")
    for error in errors:
        logging.info(f"couldn't create note for {error.verb} {error.tense}")


if __name__ == "__main__":
    main()
