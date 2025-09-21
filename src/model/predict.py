import numpy as np
import pickle
import joblib
from sklearn.pipeline import Pipeline
from model.config.core import config, PACKAGE_ROOT

def load_model():
    """Load the pre-trained model from disk."""
    with open(PACKAGE_ROOT / 'models/modelo_popularidad.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    return model

def load_scalers():
    """Load the pre-trained scalers from disk."""
    with open(PACKAGE_ROOT / 'data/train/scalers.pkl', 'rb') as scalers_file:
        scalers = joblib.load(scalers_file)
    return scalers['X']

def load_encoders():
    """Load the pre-trained encoders from disk."""
    with open(PACKAGE_ROOT / 'data/train/encoders.pkl', 'rb') as encoders_file:
        encoders = joblib.load(encoders_file)
    return encoders['categorical'], encoders['ordinal']

def initialize_pipeline() -> Pipeline:  
  """
  Initializes the data pipeline by loading the encoders, scalers, and model.

  Returns:
    Pipeline: A scikit-learn Pipeline object containing the loaded model, scalers, and encoders.
  """
  model = load_model()
  scalers = load_scalers()
  categorical_encoder, ordinal_encoder = load_encoders()

  pipeline_steps = {
    'scalers': scalers,
    'categorical_encoder': categorical_encoder,
    'ordinal_encoder': ordinal_encoder,
    'model': model
  }

  pipeline = Pipeline(steps=pipeline_steps)

  return pipeline

# Load the pre-trained model
PIPELINE = initialize_pipeline()
print("✓ Modelo cargado exitosamente!")
print(f"  • Modelo: {type(PIPELINE['model']).__name__}")
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