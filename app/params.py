import os
from dotenv import load_dotenv

if not load_dotenv():
    print("Environment variables not loaded!")

kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
kafka_topics = {
    "lv": "liveFeed"
}