from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table
)

from sqlalchemy.orm import relationship

from .database import Base


# TABLA INTERMEDIA MANY-TO-MANY

playlist_songs = Table(
    "playlist_songs",
    Base.metadata,
    Column("playlist_id", ForeignKey("playlists.id"), primary_key=True),
    Column("song_id", ForeignKey("songs.id"), primary_key=True),
)


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=True)
    genre = Column(String, nullable=True)


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    album = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    duration_seconds = Column(Integer, nullable=True)

    artist_id = Column(Integer, ForeignKey("artists.id"))
    genre_id = Column(Integer, ForeignKey("genres.id"))

    artist = relationship("Artist")
    genre = relationship("Genre")

    playlists = relationship(
        "Playlist",
        secondary=playlist_songs
    )


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    songs = relationship(
        "Song",
        secondary=playlist_songs
    )