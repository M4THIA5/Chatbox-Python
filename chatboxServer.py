import socketio
from enums import REASON

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio)
chat = []

connected_clients = set()

@sio.event
async def connect(sid, environ):
    print(f"Client connected : {sid}")
    connected_clients.add(sid)

@sio.event
async def emit_log(sid, log):
    if isinstance(log, dict) and 'reason' in log and 'userName' in log:
        for client in connected_clients:
            if client != sid:
                if log['reason'] == REASON.CONNECTION.value:
                    await sio.emit('log', f'{log["userName"]} connected', to=client)
                elif log['reason'] == REASON.DISCONNECTION.value:
                    await sio.emit('log', f'{log["userName"]} disconnected', to=client)
                else:
                    await sio.emit('log', 'Invalid log reason', to=client)

@sio.event
async def show_chat(sid):
    await sio.emit('show_chat', chat, to=sid)

@sio.event
async def disconnect(sid):
    print(f'Client disconnected : {sid}')
    connected_clients.remove(sid)

@sio.event
async def message(sid, data):
    message = {'clientId': sid, 'userName': data['userName'], 'content': data['content']}
    chat.append(message)
    for client in connected_clients:
        await sio.emit('message', message, to=client)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=4000)