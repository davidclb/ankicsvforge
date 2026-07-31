import csv
from pathlib import Path

from models.models import Sentence, Vocab


def parse_sentence(filepath: str | Path) -> list[Sentence]:
    try:
        with open(filepath, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            sentences = []
            for row in reader:
                # Skip if the the line contains a time
                if all(v == "" for k, v in row.items() if k != "transliteration"):
                    continue
                sentences.append(
                    Sentence(
                        row["topic"],
                        row["order"],
                        row["transliteration"],
                        row["meaning"],
                        row["arabic"],
                        row["source"],
                    )
                )
        return sentences
    except FileNotFoundError:
        raise
