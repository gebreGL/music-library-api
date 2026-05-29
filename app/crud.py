from sqlalchemy.orm import Session

from . import models, schemas
from .auth import hash_password


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


def create_genre(db: Session, genre: schemas.GenreCreate):
    db_genre = models.Genre(**genre.model_dump())

    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)

    return db_genre


def get_genres(db: Session):
    return db.query(models.Genre).all()


def get_genre(db: Session, genre_id: int):
    return db.query(models.Genre).filter(models.Genre.id == genre_id).first()


def create_playlist(
    db: Session,
    playlist: schemas.PlaylistCreate
):
    db_playlist = models.Playlist(
        **playlist.model_dump()
    )

    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)

    return db_playlist


def get_playlists(db: Session):
    return db.query(models.Playlist).all()


def add_song_to_playlist(
    db: Session,
    playlist_id: int,
    song_id: int
):
    playlist = (
        db.query(models.Playlist)
        .filter(models.Playlist.id == playlist_id)
        .first()
    )

    song = (
        db.query(models.Song)
        .filter(models.Song.id == song_id)
        .first()
    )

    if not playlist or not song:
        return None

    if song in playlist.songs:
        return playlist

    playlist.songs.append(song)

    db.commit()
    db.refresh(playlist)

    return playlist


def create_user(
    db: Session,
    user: schemas.UserCreate
):
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(
            user.password
        )
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_username(
    db: Session,
    username: str
):
    return (
        db.query(models.User)
        .filter(
            models.User.username == username
        )
        .first()
    )