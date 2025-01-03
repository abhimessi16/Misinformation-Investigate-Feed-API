# Misinformation Investigate
## Live Feed API

Exposing endpoints to start the investigation process. Currently supports only live data, like live news from channels online.
Exposing endpoints for emitting and streaming fake news events using server sent events.

## Requirements

    1. Python 3.12

Clone the repo - https://github.com/abhimessi16/Misinformation-Investigate-Feed-API

-    cd into repo folder
-    Create a virtual environment - recommended
-    Run - pip install -r requirements.txt
-    Create a .env file using .envExample. Add the kafka broker urls.
-    Change the kafka topic name in params file if necessary
-    Run - fastapi run app/main.py (or run using uvicorn on different port)
