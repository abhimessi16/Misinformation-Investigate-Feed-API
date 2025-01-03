from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse
import asyncio

import app.main as session
from app.models import EventInput

fact_checked_event_router = APIRouter(prefix="/v1/api/fact-check-events")

@fact_checked_event_router.post("/emit")
async def emit_event(event: EventInput):
    session.fact_check_events.append(event)
    return {"message": "sent!"}
    

@fact_checked_event_router.get("/stream")
async def stream_events(request: Request):
    async def stream_generator():
        while True:
            if await request.is_disconnected():
                break
            if len(session.fact_check_events) > 0:
                yield session.fact_check_events.popleft().model_dump_json()
            await asyncio.sleep(0.5)
    return EventSourceResponse(stream_generator())
        