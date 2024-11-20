import asyncio
import socketio
from readchar import readkey as rk

sio = socketio.AsyncClient()
RUN = True

@sio.event
async def connect():
    print('connection established')

@sio.event
async def disconnect():
    print('disconnected from server')

async def read_key():
    key = await asyncio.to_thread(rk)
    return key

@sio.event
async def message(data):
    print(data)

async def write_message():
    if not RUN:
        return
    message = input('-> ')
    await sio.emit('message', message)

async def read_mode():
    while True:
        key = await read_key()
        if key == 'q':
            global RUN
            RUN = False
            break
        elif key == ' ':
            break

async def main():
    await sio.connect('http://localhost:4000', transports=['websocket'])
    print('Welcome to the chatbox. Press SPACE to switch to write mode, Q to quit.')
    print('-----------------------------------------------------------------------\n')
    while RUN:
        await read_mode()
        await write_message()

    await sio.disconnect()

if __name__ == '__main__':
    asyncio.run(main())