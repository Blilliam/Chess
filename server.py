import asyncio
import websockets
import secrets
import json
import Constants

CONNECTED = set()
rooms = {}

async def joinRoom(ws, password):

    print(f"Password: {password} {rooms}")
    try: 
        connectedSet = rooms[password]
    except KeyError:
        print("No room found")

    event = {
        "type": "init",
        "key": password,
        "team": Constants.BLACK
    }
    await ws.send(json.dumps(event))

    connectedSet.add(ws)
    print("Other client joined")
    async for msg in ws:
        print()
        print(f"P2 sent move")
        for room in connectedSet:
            await room.send(msg)
            
            


          
async def createRoom(ws):
    roomId = secrets.token_urlsafe(10)

    roomSet = set()
    roomSet.add(ws)
    rooms[roomId] = roomSet
    print(rooms)
    try:
        event = {
            "type": "init",
            "key": roomId,
            "team": Constants.WHITE
        }
        await ws.send(json.dumps(event))
        async for msg in ws:
            print()
            print(f"P1 sent move")
            for room in roomSet:
                await room.send(msg)
    finally:
        del rooms[roomId]

    

async def handler(ws):
    CONNECTED.add(ws)
    print("connected")
    msg = await ws.recv()
    event = json.loads(msg)
    print(event)

#checks for 2nd client
    if ("key" in event):
        print(event["key"])
        await joinRoom(ws, event["key"])
        
    else:
        await createRoom(ws)
    

    # print(f"Client connected.\nClient count: {len(CONNECTED)}")

    # try:
    #     async for msg in ws:
    #         print(f"Received: {msg}")
    #         for client in CONNECTED:
    #             if client != ws:
    #                 await client.send(msg)

    # except websockets.exceptions.ConnectionClosed:
    #     pass

async def main():
    async with websockets.serve(handler, "localhost", 9001):
        print("Server at 9001")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())