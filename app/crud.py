from sqlalchemy.orm import Session

from . import models, schemas


def create_artist(db: Session, artist: schemas.ArtistCreate):
    db_artist = models.Artist(**artist.model_dump())

    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)

    return db_artist


def get_artists(db: Session):
    return db.query(models.Artist).all()

def create_song(db: Session, song: schemas.SongCreate):
    db_song = models.Song(**song.model_dump())

    db.add(db_song)
    db.commit()
    db.refresh(db_song)

    return db_song


def get_songs(db: Session):
    return db.query(models.Song).all()


def get_song(db: Session, song_id: int):
    return db.query(models.Song).filter(models.Song.id == song_id).first()