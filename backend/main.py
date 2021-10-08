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
key1 = "station1"
key2 = "station2"

@app.get("/initialize/{station_id}")
async def initialize(station_id: str):
  return db.put(0, station_id)

@app.get("/flow/{station_id}")
async def get_flow(station_id: str):
  return db.get(station_id)

@app.get("/total_flow")
async def get_total_flow():
  return db.get(key1)["value"] + db.get(key2)["value"]

@app.post("/flow/{station_id}/{more_flow}")
async def update_flow(station_id: str, more_flow: int):
  flow = db.get(station_id)
  new_flow = flow["value"] + more_flow
  # manager.broadcast(new_flow)
  return db.put(new_flow, station_id)

@app.delete("/flow/{station_id}")
async def delete_flow(station_id: str):
  return db.delete(station_id)

# unused websocket stuff:

# class ConnectionManager:
#   def __init__(self):
#     self.active_connections: List[WebSocket] = []
  
#   async def connect(self, websocket: WebSocket):
#     print('accepting client connection...')
#     await websocket.accept()
#     self.active_connections.append(websocket)

#   def disconnect(self, websocket: WebSocket):
#     self.active_connections.remove(websocket)

#   async def broadcast(self, flow: int):
#     print('broadcasting flow', flow)
#     for connection in self.active_connections:
#       await connection.send_text(flow)

# manager = ConnectionManager()

# @app.websocket("/ws")
# async def websocket(websocket: WebSocket):
#   await manager.connect(websocket)
#   try:
#     while True:
#       break
#   except WebSocketDisconnect:
#     manager.disconnect(websocket)