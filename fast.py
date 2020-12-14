import json

from fastapi import FastAPI
from pydantic import BaseModel

from tasks import add
from websocket_model import routes, broadcast

app = FastAPI(title="Test task",
              routes=routes,
              on_startup=[broadcast.connect],
              on_shutdown=[broadcast.disconnect])


class Publish(BaseModel):
    channel: str = 'task'
    message: str


@app.post("/push")
async def push_message(publish: Publish):
    await broadcast.publish(publish.channel, json.dumps(publish.message))
    return Publish(channel=publish.channel, message=publish.message)
