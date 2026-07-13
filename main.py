import logging
import sys
from urllib.error import URLError

from anki.api import invoke
import cli


def main():
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    try:
        invoke("sync")
    except URLError:
        logging.error("Anki not open, please open first anki")
        sys.exit(1)
    cli.main()


if __name__ == "__main__":
    main()
