from json import dumps
from collections import deque

from app.params import kafka_bootstrap_servers
from app.routes.live_feed_route import live_feed_router
from app.routes.fact_checked_event_route import fact_checked_event_router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from kafka import KafkaProducer

live_feed_producer = KafkaProducer(
    bootstrap_servers=kafka_bootstrap_servers,
    value_serializer=lambda data : dumps(data).encode('utf-8')
)

fact_check_events = deque()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

live_feed_app = FastAPI(middleware=middleware)

live_feed_app.include_router(live_feed_router)
live_feed_app.include_router(fact_checked_event_router)
