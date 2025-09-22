from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SongFeaturesInput(BaseModel):
    duration_ms: Optional[int]
    explicit: Optional[bool]
    danceability: Optional[float]
    energy: Optional[float]
    key: Optional[int]
    loudness: Optional[float]
    mode: Optional[int]
    speechiness: Optional[float]
    acousticness: Optional[float]
    instrumentalness: Optional[float]
    liveness: Optional[float]
    valence: Optional[float]
    tempo: Optional[float]
    time_signature: Optional[int]
    track_genre: Optional[str]


class PopularityCategory(Enum):
    NO_POPULAR = 'No popular'
    BAJA = 'Baja'
    MEDIA = 'Media'
    ALTA = 'Alta'
    DESCONOCIDA = 'Desconocida'
