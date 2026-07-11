import logging
from parsing.parser_verb import parse_verb 
import sys
from urllib.error import URLError

from anki.api import invoke

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        result = invoke('deckNames')
        logging.info(f"got list of decks: {result}") 
    except URLError:
        logging.error("Anki not open, please open first anki")
        sys.exit(1)

    try:
        filepath = "Pia_verbes.csv"
        verbs = parse_verb(filepath)
        logging.debug(verbs)
    except FileNotFoundError:
        logging.error(f"Could not open file: {filepath}")
        sys.exit(1)




if __name__=="__main__":
    main()