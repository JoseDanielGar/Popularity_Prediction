from model.predict import predict_multiclass_popularity, predict_popularity
import pandas as pd
import numpy as np

data = {
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

input_data = pd.DataFrame(data)

def test_predict_multiclass_popularity():
    prediction, probabilities = predict_multiclass_popularity(input_data)
    assert isinstance(prediction, dict)
    assert 'popularity' in prediction
    assert 'popularity_class' in prediction
    assert 'feature_relevance' in prediction
    assert isinstance(probabilities, np.ndarray)
    assert probabilities.shape[0] == 1
    assert probabilities.shape[1] == 4

def test_predict_popularity():
    prediction = predict_popularity(data)
    assert isinstance(prediction, dict)
    assert 'popularity' in prediction
    assert 'popularity_class' in prediction
    assert 'feature_relevance' in prediction

test_predict_multiclass_popularity()
test_predict_popularity()