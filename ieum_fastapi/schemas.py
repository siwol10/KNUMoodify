from pydantic import BaseModel, Field
from typing import List

class PredictRequest(BaseModel):
    text: str = Field(..., description="분류할 문장")
    emotions: List[str] | None = None
    situations:List[str] | None = None

class PredictResponse(BaseModel):
    result: str  # 예: emotion="기쁨"

class Song(BaseModel):
    artist: str
    title: str
    length: str
    emotion: str
    isrc: str
    party: int
    work: int
    relaxation: int
    exercise: int
    running: int
    stretching: int
    driving: int
    gathering: int
    morning: int
    id: str
    url: str

class WebResponse(BaseModel):
    selection: bool
    emotions: List[str]
    situations: List[str]
    songs: List[Song] | None = None