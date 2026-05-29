from fastapi import FastAPI

app = FastAPI(
    title="Music Library API",
    description="REST API for managing artists, songs, playlists and favorite tracks.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "Welcome to Music Library API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}