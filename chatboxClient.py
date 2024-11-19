import asyncio
import socketio

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('connection established')

@sio.event
async def disconnect():
    print('disconnected from server')

async def main():
    await sio.connect('http://localhost:4000')
    await asyncio.gather(sio.wait(), asyncio.sleep(5))

if __name__ == '__main__':
    asyncio.run(main())