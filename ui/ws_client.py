import asyncio
import websockets
import threading

class WSClient:
    def __init__(self, uri):
        self.uri = uri
        self.loop = asyncio.new_event_loop()
        self.messages = []
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.listen())

    async def listen(self):
        async with websockets.connect(self.uri) as websocket:
            while True:
                msg = await websocket.recv()
                self.messages.append(msg)

    def send(self, message):
        async def _send():
            async with websockets.connect(self.uri) as websocket:
                await websocket.send(message)
        asyncio.run_coroutine_threadsafe(_send(), self.loop)
