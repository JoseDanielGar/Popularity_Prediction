import logging

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse

from schemas import SongFeaturesInput, PopularityCategory

app = FastAPI(
    title="Song Popularity API",
    description="Model version: 0.1.0",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/predict")
def predict(features: SongFeaturesInput):
    # todo: make predict_popularity function receive the pipeline,
    #  we can load once the model and reuse it in the predict function (global)

    # lazy first request
    from model.predict import predict_popularity, InputFeatures, PredictionOutput

    features = InputFeatures(
        duration_ms=features.duration_ms,
        explicit=features.explicit,
        danceability=features.danceability,
        energy=features.energy,
        key=features.key,
        loudness=features.loudness,
        mode=features.mode,
        speechiness=features.speechiness,
        acousticness=features.acousticness,
        instrumentalness=features.instrumentalness,
        liveness=features.liveness,
        valence=features.valence,
        tempo=features.tempo,
        time_signature=features.time_signature,
        track_genre=features.track_genre
    )

    try:
        prediction: PredictionOutput = predict_popularity([features, ])
        logging.info("predict request completed")
        return JSONResponse(
            {"class": PopularityCategory(prediction["popularity_class"]).value},
            status.HTTP_200_OK
        )
    except Exception as exc:
        logging.error("Failed to run predict request")
        logging.error(exc)
        return JSONResponse(
            {"msg": "Failed to predict"},
            status.HTTP_503_SERVICE_UNAVAILABLE
        )


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
