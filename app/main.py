from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, SessionLocal, engine

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