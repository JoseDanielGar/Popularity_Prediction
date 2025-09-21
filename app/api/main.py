from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from model.predict import predict_popularity, InputFeatures, PredictionOutput

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
    # Convert to InputFeatures dataclass
    features = InputFeatures(
        danceability=features.danceability,
        energy=features.energy,
        acousticness=features.acousticness,
        instrumentalness=features.instrumentalness,
        valence=features.valence,
        tempo=features.tempo
    )
    prediction: PredictionOutput = predict_popularity(features)
    
    return {"predicted_popularity": prediction}
