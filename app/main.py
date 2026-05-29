from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from . import crud, models, schemas
from .database import Base, SessionLocal, engine
from .auth import (
    create_access_token,
    verify_password
)
from .auth import get_current_username

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


def get_current_user(
    username: str = Depends(get_current_username),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_username(db, username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


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
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_username(
        db,
        form_data.username
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        form_data.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "sub": db_user.username
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/me", response_model=schemas.UserResponse)
def get_me(
    current_user: models.User = Depends(get_current_user)
):
    return current_user
