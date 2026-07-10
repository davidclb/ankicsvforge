import csv
from dataclasses import dataclass

@dataclass
class Verb:
    verbe: str
    sens: str
    temps: str
    conjugaisons: dict[str, str]



with open('names.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['first_name'], row['last_name'])
