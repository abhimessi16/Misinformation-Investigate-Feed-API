import subprocess

from app.models import LiveStream
from app.params import kafka_topics
import app.main as session

def get_audio_from_m3u8_send_to_producer(m3u8_data: LiveStream, pid_store: dict):
    ffmpeg_process = subprocess.Popen(
        ['ffmpeg', '-loglevel', 'quiet', '-i', m3u8_data.m3u8_link, '-c', 'copy', '-t', '5', '-f', 'wav', 'pipe:1'],
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

def send_audio_data_to_kafka(audio_data, m3u8_data: LiveStream):
    if not audio_data:
        return
    try:
        session.live_feed_producer.send(
            topic=kafka_topics.get("lv"), 
            # key=m3u8_data.source, 
            value=audio_data
        )
    except Exception as ex:
        print(ex)
    finally:
        print(f"sent data: {len(audio_data)}.")