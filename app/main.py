from json import dumps

from app.params import kafka_bootstrap_servers
from app.routes.live_feed_route import live_feed_router

from fastapi import FastAPI
from kafka import KafkaProducer

live_feed_producer = KafkaProducer(
    bootstrap_servers=kafka_bootstrap_servers,
    value_serializer=lambda data : dumps(data).encode('utf-8')
)

live_feed_app = FastAPI()
live_feed_app.include_router(live_feed_router)