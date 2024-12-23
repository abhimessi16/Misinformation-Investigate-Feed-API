from threading import Thread
import json
import time

from fastapi import APIRouter, status
from fastapi.responses import Response

from app.models import LiveStream
from app.utils import get_audio_from_m3u8_send_to_producer

live_feed_router = APIRouter(prefix="/v1/api/live-feed")

@live_feed_router.post("/live-stream")
def live_stream(live_feed: LiveStream):
    if '.m3u8' not in live_feed.m3u8_link:
        return Response(content={"message": "Invalid stream url!"}, status_code=status.HTTP_400_BAD_REQUEST)
    
    pid_store = {}

    # get_audio_from_m3u8_send_to_producer(live_feed, pid_store)
    live_feed_thread = Thread(target=get_audio_from_m3u8_send_to_producer, args=(live_feed, pid_store,))
    live_feed_thread.daemon = True
    live_feed_thread.start()

    # there could be a slight delay by the time pid_store is populated, so sleep or something else?
    time.sleep(2)

    if pid_store.get("ffmpeg_pid"):
        return Response(content=json.dumps({
            "ffmpeg_pid": pid_store.get("ffmpeg_pid"),
            "source": live_feed.source,
        }), status_code=status.HTTP_200_OK, media_type="application/json")
    
    return Response(content=json.dumps({
        "message": "Processing of audio failed. Please try again."
    }), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@live_feed_router.post("/live-audio")
def live_audio():
    pass

@live_feed_router.post("/video-file")
def video_file():
    pass

