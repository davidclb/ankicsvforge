import logging

import sys
from urllib.error import URLError

from anki.api import invoke

def main():
    try:
        result = invoke('deckNames')
        logging.debug(f"got list of decks: {result}") 
    except URLError:
        logging.error("Anki not open, please open first anki")
        sys.exit(1)


if __name__=="__main__":
    main()