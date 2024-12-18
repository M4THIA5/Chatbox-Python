import asyncio
import socketio
from readchar import readkey as rk
import argparse
from enums import REASON
from envVariables import get_local_ip, override_env_variable, get_url

sio = socketio.AsyncClient(reconnection=True, reconnection_attempts=5, reconnection_delay=1)
USERNAME = None

@sio.event
async def connect():
    print('connection established')
    await sio.emit('emit_log', {'userName': USERNAME, 'reason': REASON.CONNECTION.value})

@sio.event
async def disconnect():
    print('disconnected from server')

@sio.event
async def log(message):
    print(message)

async def connection_url():
    try:
        await sio.connect(get_url())
        return
    except Exception as e:
        pass
    try:
        local_ip = get_local_ip()
        override_env_variable('SERVER_IP', local_ip)
        await sio.connect(get_url())
        return
    except Exception as e:
        print('Connection failed: ', e)
        return

async def read_key():
    key = await asyncio.to_thread(rk)
    return key

@sio.event
async def show_chat(chat):
    for message in chat:
        if 'userName' in message and message['userName'] != USERNAME and message['clientId'] != sio.sid:
            print(f"{message['userName']} -> {message['content']}")
        else:
            print(f"You -> {message['content']}")

@sio.event
async def message(message):
    if 'userName' in message and message['userName'] != USERNAME and message['clientId'] != sio.sid:
        print(f"{message['userName']} -> {message['content']}")

async def write_message():
    if not sio.connected:
        return
    data = {}
    data['userName'] = USERNAME
    data['content'] = input('You -> ')
    await sio.emit('message', data)

async def read_mode():
    while sio.connected:
        key = await read_key()
        if key == 'q':
            if sio.connected:
                await sio.emit('emit_log', {'userName': USERNAME, 'reason': REASON.DISCONNECTION.value})
                await sio.disconnect()
            break    
        elif key == ' ':
            break

def parse_args():
    parser = argparse.ArgumentParser(description="Chatbox client")
    parser.add_argument('--username', type=str, required=True, help="Votre nom d'utilisateur")
    args = parser.parse_args()
    return args

async def main():
    await connection_url()
    if not sio.connected:
        return
    print('Welcome to the chatbox. Press SPACE to switch to write mode, press Q to quit.')
    print('-----------------------------------------------------------------------\n')
    await sio.emit('show_chat')
    while sio.connected:
        await read_mode()
        if not sio.connected:
            break
        await write_message()
        await sio.sleep(0.1)

if __name__ == '__main__':
    args = parse_args()
    USERNAME = args.username
    asyncio.run(main())