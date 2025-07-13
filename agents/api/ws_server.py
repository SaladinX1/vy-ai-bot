from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager

app = FastAPI()
sio = SocketManager(app=app, mount='/ws')

# CORS (adapter si besoin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@ sio.on('join_workflow')
async def on_join_workflow(sid, data):
    workflow = data.get('workflow')
    await sio.enter_room(sid, workflow)
    await sio.emit('user_joined', {'user': sid}, room=workflow)

@ sio.on('edit_workflow')
async def on_edit_workflow(sid, data):
    workflow = data.get('workflow')
    changes = data.get('changes')
    # Broadcast changes to all others in room
    await sio.emit('workflow_update', {'changes': changes, 'user': sid}, room=workflow, skip_sid=sid)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
