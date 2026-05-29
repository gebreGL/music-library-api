from sqlalchemy import Column, Integer, String
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=True)
    genre = Column(String, nullable=True)

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    album = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)

    artist = relationship("Artist")