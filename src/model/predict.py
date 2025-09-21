import numpy as np
import pickle
import joblib
from sklearn.pipeline import Pipeline
from config.core import config, ROOT

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

def initialize_pipeline() -> Pipeline:  
  """
  Initializes the data pipeline by loading the encoders, scalers, and model.

  Returns:
    Pipeline: A scikit-learn Pipeline object containing the loaded model, scalers, and encoders.
  """
  model = load_model()
  scalers = load_scalers()
  encoders = load_encoders()

  scalers['duration_ms_scaler'].transform([[73]])
  scalers['loudness_scaler'].transform([[-6.746]])
  scalers['tempo_scaler'].transform([[87.917]])

  encoders['key_label_encoder'].transform(['1'])
  encoders['track_genre_label_encoder'].transform(['acoustic'])

  pipeline_steps = [
    #('duration_ms_scaler', scalers['duration_ms_scaler']),
    #('loudness_scaler', scalers['loudness_scaler']),
    #('tempo_scaler', scalers['tempo_scaler']),
    #('key_label_encoder', encoders['key_label_encoder']),
    #('track_genre_label_encoder', encoders['track_genre_label_encoder']),
    ('model', model)
  ]

  pipeline = Pipeline(steps=pipeline_steps)

  return pipeline


def predict_multiclass(input_array: np.ndarray):
  """
  Predicts a multiclass output and their corresponding probabilities using a pre-trained model.

  Args:
    input_array (np.ndarray): Input data for prediction.

  Returns:
    tuple: A tuple containing the predicted class and the probabilities for each class.
  """
  # Ensure the input is a 2D array
  if input_array.ndim == 1:
    input_array = input_array.reshape(1, -1)

  # Predict probabilities
  probabilities = PIPELINE.predict_proba(input_array)

  # Predict the class
  predicted_class = PIPELINE.predict(input_array)

  return predicted_class, probabilities


# Load the pre-trained model
PIPELINE = initialize_pipeline()
print("✓ Modelo cargado exitosamente!")
print(f"  • Modelo: {type(PIPELINE['model']).__name__}")
print(PIPELINE)
y_pred = PIPELINE.predict(np.array([[230666,False,0.676,0.461,1,-6.746,0,0.143,0.0322,1.01e-06,0.358,0.715,87.917,4,'acoustic']]))  # Example prediction
print(y_pred)