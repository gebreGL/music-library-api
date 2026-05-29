from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, SessionLocal, engine
from .auth import (
    create_access_token,
    verify_password
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Music Library API",
    description="REST API for managing artists, songs, playlists and favorite tracks.",
    version="0.1.0",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Welcome to Music Library API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/artists", response_model=schemas.ArtistResponse)
def create_artist(
    artist: schemas.ArtistCreate,
    db: Session = Depends(get_db)
):
    return crud.create_artist(db, artist)


@app.get("/artists", response_model=list[schemas.ArtistResponse])
def get_artists(
    db: Session = Depends(get_db)
):
    return crud.get_artists(db)


@app.post("/songs", response_model=schemas.SongResponse)
def create_song(
    song: schemas.SongCreate,
    db: Session = Depends(get_db)
):
    return crud.create_song(db, song)


@app.get("/songs", response_model=list[schemas.SongResponse])
def get_songs(
    db: Session = Depends(get_db)
):
    return crud.get_songs(db)


@app.get("/songs/{song_id}", response_model=schemas.SongResponse)
def get_song(
    song_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_song(db, song_id)


@app.post("/genres", response_model=schemas.GenreResponse)
def create_genre(
    genre: schemas.GenreCreate,
    db: Session = Depends(get_db)
):
    return crud.create_genre(db, genre)


@app.get("/genres", response_model=list[schemas.GenreResponse])
def get_genres(
    db: Session = Depends(get_db)
):
    return crud.get_genres(db)


@app.get("/genres/{genre_id}", response_model=schemas.GenreResponse)
def get_genre(
    genre_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_genre(db, genre_id)


@app.post(
    "/playlists",
    response_model=schemas.PlaylistResponse
)
def create_playlist(
    playlist: schemas.PlaylistCreate,
    db: Session = Depends(get_db)
):
    return crud.create_playlist(db, playlist)


@app.get(
    "/playlists",
    response_model=list[schemas.PlaylistResponse]
)
def get_playlists(
    db: Session = Depends(get_db)
):
    return crud.get_playlists(db)


@app.post(
    "/playlists",
    response_model=schemas.PlaylistResponse
)
def create_playlist(
    playlist: schemas.PlaylistCreate,
    owner_id: int | None = None,
    db: Session = Depends(get_db)
):
    return crud.create_playlist(
        db,
        playlist,
        owner_id
    )


@app.post(
    "/register",
    response_model=schemas.UserResponse
)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(
        db,
        user
    )


@app.post("/login")
def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_username(
        db,
        user.username
    )

    if not db_user:
        return {"error": "Invalid credentials"}

    if not verify_password(
        user.password,
        db_user.hashed_password
    ):
        return {"error": "Invalid credentials"}

    token = create_access_token(
        {
            "sub": db_user.username
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }