from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from database.connection import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    classification = Column(String)
    name = Column(String)
    type1 = Column(String)
    type2 = Column(String)
    generation = Column(Integer)
    
    stats = relationship("Stats", back_populates="pokemon")


class Stats(Base):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"))
    height_m = Column(Float)
    weight_kg = Column(Float)
    attack = Column(Integer)
    defense = Column(Integer)
    hp = Column(Integer)
    speed = Column(Integer)

    pokemon = relationship("Pokemon", back_populates="stats")

