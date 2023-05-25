from database.models import Pokemon, PokemonStats
import csv

def uploadCSVFileToPokemonDatabase(file, db):
    fileContent = file.file.read().decode("utf-8")
    rows = csv.reader(fileContent.splitlines(), delimiter=",")
    next(rows)  # Skip the first row (column names)

    for row in rows:
        pokemon = Pokemon(classification=row[1], name=row[3], type1=row[5], type2=row[6], generation=row[7])
        db.add(pokemon)

    db.commit()

import csv

def uploadCSVFileToPokemonStatsDatabase(file, db):
    fileContent = file.file.read().decode("utf-8")
    rows = csv.reader(fileContent.splitlines(), delimiter=",")
    next(rows)  # Skip the first row (column names)

    for row in rows:
        pokemonStats = PokemonStats(pokemon_id=row[0], height_m=row[26] if row[26] else None, weight_kg=row[31] if row[31] else None, attack=row[19])
        db.add(pokemonStats)

    db.commit()
