from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    city: str
    location: Optional[str] = None
    category: Optional[str] = None
    event_date: Optional[datetime] = None
    source_name: str
    source_url: str


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True