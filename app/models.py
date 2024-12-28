# to do or not to do?

from pydantic import BaseModel
from datetime import datetime

class LiveStream(BaseModel):
    m3u8_link: str
    source: str
    timestamp: datetime
    session_id: str