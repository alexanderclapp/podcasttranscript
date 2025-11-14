from pydantic import BaseModel, HttpUrl
from typing import Optional


class PodcastRequest(BaseModel):
    url: HttpUrl


class PodcastResponse(BaseModel):
    transcript: str
    summary: str
    metadata: Optional[dict] = None

