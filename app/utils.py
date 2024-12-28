import subprocess
import os, signal

from app.models import LiveStream
from app.params import kafka_topics
import app.main as session

def get_audio_from_m3u8_send_to_producer(m3u8_data: LiveStream, pid_store: dict):
    # add a retry mechanism, check how?
    ffmpeg_process = subprocess.Popen(
        ['ffmpeg', '-loglevel', 'quiet', '-i', m3u8_data.m3u8_link, '-t', '1', '-f', 'wav', 'pipe:1'], # duration of 1 for now, add ac -1 later
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    pid_store['ffmpeg_pid'] = ffmpeg_process.pid
    print(f"FFMPEG process started, PID is {ffmpeg_process.pid}")
    
    while audio_data := ffmpeg_process.stdout.read(1024):
        if not audio_data:
            break
        send_audio_data_to_kafka(audio_data, m3u8_data)

    session.live_feed_producer.flush()

def send_audio_data_to_kafka(audio_data: bytes, m3u8_data: LiveStream):
    if not audio_data:
        return
    
    produced_data = {
        "source": m3u8_data.source,
        "audio_data": audio_data.decode("utf-16le"),
        "session_id": m3u8_data.session_id
    }
    try:
        session.live_feed_producer.send(
            topic=kafka_topics.get("lv"), 
            # key=m3u8_data.source, # gonna implement this later
            value=produced_data
        )
        # waiting for the data to be sent is not the best idea,
        # it kinda beats the purpose of real-time syncing of data
    except Exception as ex:
        # what can we do if an exception arises
        print(ex)
    finally:
        # what can we do finally
        print(f"sent data: {len(audio_data)}.")

def kill_subprocess(pid: int):
    os.kill(pid, signal.SIGTERM)