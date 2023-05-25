from fastapi import APIRouter, Depends, File, UploadFile
from typing import Annotated
from schemas.pokemon import Pokemon
from database.connection import get_db
from database.models import Pokemon as PokemonTableModel
from database.models import Stats as PokemonStatsModel
from sqlalchemy.orm import Session, subqueryload
import csv



router = APIRouter(prefix="/pokemon", tags=["pokemon"])


@router.get("/")
def getAllPokemon(db: Session = Depends(get_db)):
    item = db.query(PokemonTableModel).all()
    return item

from fastapi import HTTPException

@router.get("/id/{pokemon_id}")
def getPokemonStats(pokemon_id: int, db: Session = Depends(get_db)):
    pokemon = db.query(PokemonTableModel).filter(PokemonTableModel.id == pokemon_id).first()
    if pokemon:
        stats = pokemon.stats
        return pokemon
    else:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    
from fastapi import HTTPException

@router.get("/{pokemon_name}")
def getPokemonByName(pokemon_name: str, db: Session = Depends(get_db)):
    item = db.query(PokemonTableModel).filter(PokemonTableModel.name.ilike(f"%{pokemon_name}%")).first()
    if item:
        return {"data": item}
    else:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    

@router.get("/stats/{pokemon_name}")
def getPokemonStatsByName(pokemon_name: str, db: Session = Depends(get_db)):
    pokemon = db.query(PokemonTableModel).filter(PokemonTableModel.name.ilike(f"%{pokemon_name}%")).first()
    if pokemon:
        stats = db.query(PokemonStatsModel).filter(PokemonStatsModel.pokemon_id == pokemon.id).first()
        if stats:
            return stats
        else:
            raise HTTPException(status_code=404, detail="Pokemon stats not found")
    else:
        raise HTTPException(status_code=404, detail="Pokemon not found")




@router.post("/pokemon/")
def CSVToPokemonDatabase(file: UploadFile, db: Session = Depends(get_db)):
    fileContent = file.file.read().decode("utf-8")
    rows = csv.reader(fileContent.splitlines(), delimiter=",")
    next(rows)
    for row in rows:
        pokemon = PokemonTableModel(id=row[0], classification=row[1], name=row[3], type1=row[5], type2=row[6], generation=row[7])
        db.add(pokemon)
    db.commit()

@router.post("/stats/")
def CSVToStatsDatabase(file: UploadFile, db: Session = Depends(get_db)):
    fileContent = file.file.read().decode("utf-8")
    rows = csv.reader(fileContent.splitlines(), delimiter=",")
    next(rows)
    for row in rows:
        pokemonStats = PokemonStatsModel(pokemon_id=int(row[0]), height_m=row[26] if row[26] else None, weight_kg=row[31] if row[31] else None, attack=row[19], defense = row[24], hp = row[27], speed = row[30])
        db.add(pokemonStats)
    db.commit()

@router.post("/")
def AddPokemon(pokemon: Pokemon, db: Session = Depends(get_db)):
    pokemon_data = PokemonTableModel(name = pokemon.name,
                                     classification = pokemon.classification,
                                     type1 = pokemon.type1,
                                     type2 = pokemon.type2,
                                     percentage_male = pokemon.percentage_male,
                                     generation = pokemon.generation)
                                     
    db.add(pokemon_data)
    db.commit()
    db.refresh(pokemon_data)
    return ("Item Added" + pokemon_data)

    