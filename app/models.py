# to do or not to do?

from pydantic import BaseModel
from datetime import datetime

class LiveStream(BaseModel):
    m3u8_link: str
    source: str
    timestamp: datetime
    session_id: str

class EventInput(BaseModel):
    source: str
    session_id: str
    audio_data: str
    fact_source: str