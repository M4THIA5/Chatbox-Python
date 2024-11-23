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
    for message in chat:
        await sio.emit('message', f"{message['clientId']} -> {message['content']}", to=sid)

@sio.event
async def disconnect(sid):
    print(f'Client disconnected : {sid}')
    connected_clients.remove(sid)

@sio.event
async def message(sid, data):
    chat.append({'clientId': sid, 'content': data})
    print(f"Message recieve by {sid} : {data}")
    for client in connected_clients:
        if client != sid:
            await sio.emit('message', f"{sid} -> {data}", to=client)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=4000)