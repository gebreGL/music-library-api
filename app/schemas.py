from pydantic import BaseModel


class ArtistBase(BaseModel):
    name: str
    country: str | None = None
    genre: str | None = None


class ArtistCreate(ArtistBase):
    pass


class ArtistResponse(ArtistBase):
    id: int

    class Config:
        from_attributes = True


class SongBase(BaseModel):
    title: str
    album: str | None = None
    year: int | None = None
    duration_seconds: int | None = None
    artist_id: int


class SongCreate(SongBase):
    pass


class SongResponse(SongBase):
    id: int

    class Config:
        from_attributes = True