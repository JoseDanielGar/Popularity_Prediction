import numpy as np
import pickle
import joblib
from sklearn.pipeline import Pipeline
from config.core import ROOT
import pandas as pd
from typing import TypedDict

class InputFeatures(TypedDict):
  duration_ms: int
  explicit: bool
  danceability: float
  energy: float
  key: int
  loudness: float
  mode: int
  speechiness: float
  acousticness: float
  instrumentalness: float
  liveness: float
  valence: float
  tempo: float
  time_signature: int
  track_genre: str

class PredictionOutput(TypedDict):
  popularity: int
  popularity_class: str
  feature_relevance: dict

def load_model():
    """Load the pre-trained model from disk."""
    with open(ROOT / 'models/modelo_popularidad.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    return model

def load_scalers():
    """Load the pre-trained scalers from disk."""
    with open(ROOT / 'data/train/scalers.joblib', 'rb') as scalers_file:
        scalers = joblib.load(scalers_file)
    return scalers

def load_encoders():
    """Load the pre-trained encoders from disk."""
    with open(ROOT / 'data/train/encoders.joblib', 'rb') as encoders_file:
        encoders = joblib.load(encoders_file)
    return encoders

def load_preprocessor():
    """Load the pre-trained preprocessor from disk."""
    with open(ROOT / 'data/train/preprocessor.joblib', 'rb') as preprocessor_file:
        preprocessor = joblib.load(preprocessor_file)
    return preprocessor

def initialize_pipeline() -> Pipeline:  
  """
  Initializes the data pipeline by loading the encoders, scalers, and model.

  Returns:
    Pipeline: A scikit-learn Pipeline object containing the loaded model, scalers, and encoders.
  """
  model = load_model()
  scalers = load_scalers()
  encoders = load_encoders()
  preprocessor = load_preprocessor()

  scalers['duration_ms_scaler'].transform([[1.01e-06]])
  scalers['loudness_scaler'].transform([[-6.746]])
  scalers['tempo_scaler'].transform([[87.917]])

  encoders['key_label_encoder'].transform(['1'])
  encoders['track_genre_label_encoder'].transform(['acoustic'])

  pipeline_steps = [
    ('preprocess', preprocessor),
    ('model', model)
  ]

  pipeline = Pipeline(steps=pipeline_steps)

  return pipeline


def predict_multiclass_popularity(input: pd.DataFrame) -> tuple:
  """
  Predicts a multiclass output and their corresponding probabilities using a pre-trained model.

  Args:
    input (pd.DataFrame): Input data for prediction.

  Returns:
    tuple: A tuple containing the predicted class and the probabilities for each class.
  """

  # Predict probabilities
  probabilities = PIPELINE.predict_proba(input)

  # Predict the class
  predicted_popularity = PIPELINE.predict(input)
  # Map predicted popularity to class labels
  # 0 = 'No popular', 1 = 'Baja', 2 = 'Media', 3 = 'Alta'
  predicted_class = {0: 'No popular', 1: 'Baja', 2: 'Media', 3: 'Alta'}.get(predicted_popularity[0], 'Desconocida')
  prediction = {
    "popularity": int(predicted_popularity[0]),
    "popularity_class": str(predicted_class),
    "feature_relevance": {}
  }

  return prediction, probabilities

def predict_popularity(input: InputFeatures) -> PredictionOutput:
  """
  Predicts the popularity of a track using a pre-trained model.

  Args:
    input (InputFeatures): Input features for prediction.

  Returns:
    np.ndarray: The predicted popularity score.
  """
  # Convert input features to DataFrame
  input_df = pd.DataFrame(input)

  # Make prediction
  predicted_popularity = PIPELINE.predict(input_df)
  # Map predicted popularity to class labels
  # 0 = 'No popular', 1 = 'Baja', 2 = 'Media', 3 = 'Alta'
  predicted_class = {0: 'No popular', 1: 'Baja', 2: 'Media', 3: 'Alta'}.get(predicted_popularity[0], 'Desconocida')
  return {
    "popularity": int(predicted_popularity[0]),
    "popularity_class": str(predicted_class),
    "feature_relevance": {}
  }

# Load the pre-trained model
PIPELINE = initialize_pipeline()
print("✓ Modelo cargado exitosamente!")
print(f"  • Modelo: {type(PIPELINE['model']).__name__}")
""" data = {
  "duration_ms": [230666],
  "explicit": [False],
  "danceability": [0.676],
  "energy": [0.461],
  "key": [1],
  "loudness": [-6.746],
  "mode": [0],
  "speechiness": [0.143],
  "acousticness": [0.0322],
  "instrumentalness": [1.01e-06],
  "liveness": [0.358],
  "valence": [0.715],
  "tempo": [87.917],
  "time_signature": [4],
  "track_genre": ["acoustic"]
}

df = pd.DataFrame(data)
print(df)
y_pred, y_proba = predict_multiclass_popularity(df)
print(y_pred)
print(y_proba)
popularity = predict_popularity(data)
print(popularity) """