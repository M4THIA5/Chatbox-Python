import socketio

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio)
chat = []

connected_clients = set()

@sio.event
async def connect(sid, environ):
    print(f"Client connected : {sid}")
    connected_clients.add(sid)

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