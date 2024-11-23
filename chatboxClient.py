import asyncio
import socketio
from readchar import readkey as rk
import argparse

sio = socketio.AsyncClient(reconnection=True, reconnection_attempts=5, reconnection_delay=1)
RUN = True

@sio.event
async def connect():
    print('connection established')

@sio.event
async def disconnect():
    print('disconnected from server')

@sio.event
async def connect_error():
    print('connection failed')

async def read_key():
    key = await asyncio.to_thread(rk)
    return key

@sio.event
async def show_chat(data):
    print(data)

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
    print('Welcome to the chatbox. Press SPACE to switch to write mode, press Q to quit.')
    print('-----------------------------------------------------------------------\n')
    await sio.emit('show_chat')
    while RUN:
        await read_mode()
        await write_message()
        await sio.sleep(0.1)

    await sio.disconnect()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chatbox client")
    parser.add_argument('--username', type=str, required=True, help="Votre nom d'utilisateur")
    args = parser.parse_args()

    #TODO: Add the username to the message
    username = args.username
    asyncio.run(main())