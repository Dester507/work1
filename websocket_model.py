from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute
from starlette.concurrency import run_until_first_complete

from broadcaster import Broadcast
from tasks import add

broadcast = Broadcast("redis://localhost:6379")


class Echo(WebSocketEndpoint):
    encoding = 'text'

    async def on_connect(self, websocket):
        await websocket.accept()

    async def on_receive(self, websocket, data):
        await websocket.send_text(f"Message text was: {data}")

    async def on_disconnect(self, websocket, close_code):
        pass


async def events_ws(websocket):
    await websocket.accept()
    await run_until_first_complete((events_ws_receiver, {"websocket": websocket}),
                                   (events_ws_sender, {"websocket": websocket}))


async def events_ws_receiver(websocket):
    async for message in websocket.iter_text():
        await broadcast.publish(channel='task', message=message)


async def events_ws_sender(websocket):
    async with broadcast.subscribe(channel='task') as subscriber:
        async for event in subscriber:
            ans = add.apply_async(([event.message]), serializer="json") # celery task
            await websocket.send_text(ans.get())


routes = [WebSocketRoute("/ws", Echo),
          WebSocketRoute("/events", events_ws, name="events_ws")]
