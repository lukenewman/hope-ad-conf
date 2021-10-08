from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from deta import Deta
from typing import List

app = FastAPI()
origins = ["http://localhost:3001"]
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

deta = Deta('b0notwt2_HNE4eF4bg3VcYDGhypaECPB2zwDzFHg6')
db = deta.Base("flow")
key = "flow"

class ConnectionManager:
  def __init__(self):
    self.active_connections: List[WebSocket] = []
  
  async def connect(self, websocket: WebSocket):
    print('accepting client connection...')
    await websocket.accept()
    self.active_connections.append(websocket)

  def disconnect(self, websocket: WebSocket):
    self.active_connections.remove(websocket)

  async def broadcast(self, flow: int):
    print('broadcasting flow', flow)
    for connection in self.active_connections:
      await connection.send_text(flow)

manager = ConnectionManager()

@app.get("/initialize")
async def initialize():
  return db.put(0, key)

@app.get("/flow")
async def get_flow():
  return db.get(key)

@app.post("/flow/{more_flow}")
async def update_flow(more_flow: int):
  flow = db.get(key)
  print(flow)
  new_flow = flow["value"] + more_flow
  manager.broadcast(new_flow)
  return db.put(new_flow, key)

@app.delete("/flow")
async def delete_flow():
  return db.delete(key)

@app.websocket("/ws")
async def websocket(websocket: WebSocket):
  await manager.connect(websocket)
  try:
    while True:
      break
  except WebSocketDisconnect:
    manager.disconnect(websocket)