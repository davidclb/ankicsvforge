import csv
from pathlib import Path
import sys
from models.verb import Verb
PRONOUNS = ['ana', 'enta', 'ente', 'houwe', 'hiye', 'nehna', 'ento', 'henne']

def parse_verb(filepath: str | Path) -> list[Verb]:
    try:
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            verbs=[]
            for row in reader:
                if all(v == "" for k, v in row.items() if k != "verb"):
                    continue
                verbs.append(Verb(row['verb'], 
                                  row['meaning'], 
                                  row['tense'], 
                                  {p: row[p] for p in PRONOUNS if row[p]},
                                  row['arab']))
        return verbs
    except FileNotFoundError:
       raise 