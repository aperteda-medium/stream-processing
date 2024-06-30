from fastapi import Depends, FastAPI

from routes import event_stream

app = FastAPI()

app.include_router(event_stream.router)