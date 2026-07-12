import logging
from anki.actions import (
    add_notes,
    check_model,
    create_conjugation_deck,
    create_conjugation_model,
)
from parsing.parser_verb import parse_verb
import sys
from urllib.error import URLError

from anki.api import invoke


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    try:
        invoke("sync")
    except URLError:
        logging.error("Anki not open, please open first anki")
        sys.exit(1)

    try:
        filepath = "example_verbes.csv"
        verbs = parse_verb(filepath)
        logging.debug(verbs)
    except FileNotFoundError:
        logging.error(f"Could not open file: {filepath}")
        sys.exit(1)
    create_conjugation_model()
    create_conjugation_deck()
    for verb in verbs:
        add_notes(verb)


if __name__ == "__main__":
    main()
