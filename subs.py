import json
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed


async def connect(url):
    async with websockets.connect(url) as websocket:
        print("Приїднався...")
        while True:
            message = await websocket.recv()
            try:
                action = json.loads(message)
                print(action)
            except:
                print(message)
            

async def hello():
    url = "ws://localhost:8000/events"
    try:
        await connect(url)
    except ConnectionClosed:
        await asyncio.sleep(3)
        print("Не вийшло приїднатись, спробую ще раз за 3с")
        await connect(url)


asyncio.get_event_loop().run_until_complete(hello())