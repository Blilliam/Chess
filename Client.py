import websockets
import asyncio
import json
import threading
from queue import Empty, Queue

class Client:
    def __init__(self):
        self.url = "ws://localhost:9001"
        self.thread = None
        self.loop = None
        self.websocket = None
        self.connected = threading.Event()
        self.pendingMessages = Queue()

    def connect(self):
        self.thread = threading.Thread(target = self.run, daemon = True)
        self.thread.start()
    def startGame(self):
        ...

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.receiveMessages())

    async def receiveMessages(self):
        try:
            async with websockets.connect(self.url) as websocket:
                self.websocket = websocket
                self.connected.set()
                print("client connect")
                async for message in websocket:
                    self.pendingMessages.put(json.loads(message))
        except Exception as e:
            print(type(e).__name__, e)

    def sendMsg(self, txt):
        if self.loop is not None and self.websocket is not None:
            asyncio.run_coroutine_threadsafe(self.websocket.send(json.dumps(txt)), self.loop)

    def requestJoin(self, key):
        if key == "":
            event = {
                "type" : "createRoom"
            }
            
        else:
            event = {
                "type" : "joinRoom",
                "key" : key
            }

        if not self.connected.wait(timeout=5):
            print("timed out")
            return False

        asyncio.run_coroutine_threadsafe(
            self.websocket.send(json.dumps(event)),
            self.loop
        )

    def poll(self):
        messages = []

        while True:
            try:
                messages.append(self.pendingMessages.get_nowait())
            except Empty:
                break
        return messages
