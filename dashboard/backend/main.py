from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173", "http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SongFeatures(BaseModel):
    danceability: float
    energy: float
    acousticness: float
    instrumentalness: float
    valence: float
    tempo: float

@app.post("/api/predict")
def predict(features: SongFeatures):
    # Mock simple scoring logic
    score = (
        features.danceability * 0.35
        + features.energy * 0.25
        + features.valence * 0.20
        + (1 - features.acousticness) * 0.10
        + (1 - features.instrumentalness) * 0.07
        + ((features.tempo - 50) / 150) * 0.03
    )
    score = max(0, min(1, score))
    return {"score": score}


@app.get("/api/health")
def health():
    JSONResponse(
        {
            "app_name": "Song Popularity API",
            "app_version": "1.0.0"
        },
        status.HTTP_200_OK
    )

@app.get("/")
def app_socket():
    return health()
