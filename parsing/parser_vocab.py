import csv
from pathlib import Path

from models.models import Vocab


def parse_vocab(filepath: str | Path) -> list[Vocab]:
    try:
        with open(filepath, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            vocabs = []
            for row in reader:
                # Skip if the the line contains a time
                if all(v == "" for k, v in row.items() if k != "transliteration"):
                    continue
                vocabs.append(
                    Vocab(
                        row["transliteration"],
                        row["meaning"],
                        row["arab"],
                    )
                )
        return vocabs
    except FileNotFoundError:
        raise
