import csv
from pathlib import Path

from models.models import Sentence


def parse_sentence(filepath: str | Path) -> list[Sentence]:
    try:
        with open(filepath, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            sentences = []
            for row in reader:
                # skip date separator lines (only 'topic' filled)
                if all(v == "" for k, v in row.items() if k != "topic"):
                    continue
                sentences.append(
                    Sentence(
                        row["topic"],
                        row["order"],
                        row["type"],
                        row["transliteration"],
                        row["meaning"],
                        row["arabic"],
                        row["source"],
                    )
                )
        return sentences
    except FileNotFoundError:
        raise
