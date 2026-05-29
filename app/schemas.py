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