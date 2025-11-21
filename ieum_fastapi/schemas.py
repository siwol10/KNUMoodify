from pydantic import BaseModel, Field
from typing import List

class Request(BaseModel):
    text: str = Field(..., description="분류할 문장")
    emotions: List[str] | None = None
    situations:List[str] | None = None

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

class Response(BaseModel):
    selection: bool
    emotions: List[str]
    situations: List[str]
    songs: List[Song] | None = None

class PlaylistRequest(BaseModel):
    track_ids: List[str]
    name: str = "IEUM 추천 플레이리스트"

class LoginResponse(BaseModel):
    authorize_url: str