import socketio

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio)

connected_clients = set()

@sio.event
async def connect(sid, environ):
    print(f"Client connecté : {sid}")
    connected_clients.add(sid)

@sio.event
async def disconnect(sid):
    print(f'Client déconnecté : {sid}')
    connected_clients.remove(sid)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=4000)