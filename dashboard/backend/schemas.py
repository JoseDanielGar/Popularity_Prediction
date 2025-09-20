import joblib
import pandas as pd
from pydantic import BaseModel
from typing import Dict, Tuple, Any


class SongFeaturesInput(BaseModel):
    """
    Clase de entrada que define las características (features) que recibe el modelo.
    Cada campo incluye su tipo de dato esperado.

    Parameters:
        duration_ms (float): Duración de la canción en milisegundos.
        explicit (bool): Indica si la canción es explícita.
        danceability (float): Medida de qué tan bailable es la canción (0.0 a 1.0).
        energy (float): Nivel de energía de la canción (0.0 a 1.0).
        key (int): Tono musical codificado como entero.
        loudness (float): Volumen promedio en decibelios (dB).
        speechiness (float): Proporción de palabras habladas (0.0 a 1.0).
        acousticness (float): Probabilidad de que la canción sea acústica (0.0 a 1.0).
        instrumentalness (float): Probabilidad de que sea instrumental (0.0 a 1.0).
        liveness (float): Presencia de público en vivo (0.0 a 1.0).
        valence (float): Positividad emocional (0.0 a 1.0).
        tempo (float): Velocidad de la canción en BPM.
        track_genre (int): Género musical codificado como número entero.
        mode_1 (bool): Indica si está en modo mayor (True/False).
        time_signature_1 (bool): Compás 1.
        time_signature_3 (bool): Compás 3.
        time_signature_4 (bool): Compás 4.
        time_signature_5 (bool): Compás 5.
    """

    duration_ms: float
    explicit: bool
    danceability: float
    energy: float
    key: int
    loudness: float
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    track_genre: int
    mode_1: bool
    time_signature_1: bool
    time_signature_3: bool
    time_signature_4: bool
    time_signature_5: bool


class SongFeaturesOutput(BaseModel):
    """
    Clase de salida que representa el resultado de la predicción.

    Parameters:
        label (str): Etiqueta predicha por el modelo ("0" = No Popular, "1" = Popular).
    """

    label: str


def get_feature_ranges(path: str = "data/train/X_train.csv") -> Dict[str, Any]:
    """
    Obtiene los rangos o valores únicos de cada variable a partir del dataset de entrenamiento.

    Parameters:
        path (str): Ruta al archivo CSV con las características de entrenamiento.

    Returns:
        Dict[str, Any]: Diccionario con los nombres de las variables como llave.
            - Si la variable es numérica retorna una tupla con (min, max).
            - Si es categórica retorna una lista de valores únicos.
    """
    X_train = pd.read_csv(path)

    feature_ranges = {}
    for col in X_train.columns:
        if pd.api.types.is_numeric_dtype(
            X_train[col]
        ):  # Si es numérica: devuelve el mínimo y máximo.
            feature_ranges[col] = (X_train[col].min(), X_train[col].max())
        else:  # Si es categórica: devuelve la lista de valores únicos.
            feature_ranges[col] = list(X_train[col].unique())

    return feature_ranges


def load_model(model_path: str = "models/classifier_model.pkl"):
    """
    Carga un modelo previamente entrenado desde un archivo .pkl.

    Parameters:
        model_path (str): Ruta al archivo del modelo serializado con joblib.

    Returns:
        Any: Objeto del modelo cargado (ej: XGBoostClassifier).
    """
    return joblib.load(model_path)


def predict_song_label(
    input_data: SongFeaturesInput, model_path: str = "models/classifier_model.pkl"
) -> SongFeaturesOutput:
    """
    Realiza una predicción sobre si una canción será popular o no.

    Parameters:
        input_data (SongFeaturesInput): Objeto con las características de entrada validadas.
        model_path (str): Ruta al archivo del modelo entrenado (.pkl).

    Returns:
        SongFeaturesOutput: Objeto con la etiqueta predicha ("0" o "1").
    """

    # 1. Cargar el modelo desde pkl.
    model = load_model(model_path)

    # 2. Convertir entrada Pydantic a DataFrame.
    df = pd.DataFrame([input_data.model_dump()])

    # 3. Predecir.
    prediction = model.predict(df)[0]

    return SongFeaturesOutput(label=str(prediction))


if __name__ == "__main__":
    # Ejemplo de entrada con los tipos correctos:
    song = SongFeaturesInput(
        duration_ms=210000.0,
        explicit=True,
        danceability=0.7,
        energy=0.8,
        key=5,
        loudness=-6.0,
        speechiness=0.05,
        acousticness=0.1,
        instrumentalness=0.0,
        liveness=0.1,
        valence=0.6,
        tempo=120.0,
        track_genre=5,
        mode_1=False,
        time_signature_1=False,
        time_signature_3=False,
        time_signature_4=True,
        time_signature_5=False,
    )

    # Obtener predicción.
    output = predict_song_label(song)
    print(output.model_dump_json())
