from pydantic import BaseModel, HttpUrl
from typing import Optional, List


class PodcastRequest(BaseModel):
    url: HttpUrl


class PodcastResponse(BaseModel):
    transcript: str
    summary: str  # Type 1 summary
    summary_type_2: Optional[str] = None  # Type 2 structured summary
    metadata: Optional[dict] = None
    summary_id: Optional[int] = None  # Database ID


class SummaryListItem(BaseModel):
    id: int
    podcast_url: str
    podcast_title: Optional[str]
    summary_type_1: str
    summary_type_2: Optional[str]
    created_at: str
    metadata: Optional[dict] = None


class SummariesListResponse(BaseModel):
    summaries: List[SummaryListItem]

