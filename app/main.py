import flask
import psycopg2

from flask import request
from pydantic import BaseModel, ValidationError
from decouple import config

DATABASE_URL = config("DATABASE_URL")

app = flask.Flask(__name__)

def connect_db():
    return psycopg2.connect(DATABASE_URL)

INSERT_ROOM_SQL = """
  INSERT INTO Rooms (name, description, enable, start_date, end_date, created_at, updated_at)
  VALUES (%(name)s, %(description)s, %(enable)s, %(start_date)s, %(end_date)s, %(created_at)s, %(updated_at)s)
"""

GET_ROOMS_SQL = """
  SELECT * FROM Rooms
"""

GET_ROOM_SQL = """
  SELECT * FROM Rooms WHERE id = %(id)s
"""

UPDATE_ROOM_SQL = """
  UPDATE Rooms SET name = %(name)s, description = %(description)s, enable = %(enable)s, start_date = %(start_date)s, end_date = %(end_date)s, updated_at = %(updated_at)s
  WHERE id = %(id)s
"""

DELETE_ROOM_SQL = """
  DELETE FROM Rooms WHERE id = %(id)s
"""

class RoomBase(BaseModel):
  name: str
  description: str
  enable: bool
  start_date: str
  end_date: str
  created_at: str
  updated_at: str

class RoomCreate(RoomBase):
  ...

class Room(RoomBase):
  id: int

@app.route("/api/v1/rooms", methods=["POST"])
def create_room():
  try:
    params = request.json
    room = RoomCreate(**params)
    return room.model_dump(), 202
  except ValidationError as e:
    return e.errors(), 400
    
@app.route("/api/v1/rooms/<room_id>", methods=["DELETE"])
def remover_room(room_id):
  return f"Remover sala com ID {room_id}", 200

@app.route("/api/v1/rooms/<room_id>", methods=["PUT"]) # CASO PRATICO: QUAL A DIFERENCA ENTRE PUT E PATCH?
def update_room(room_id):
  try:
    params = request.json
    room = RoomCreate(**params)
    print(f"Atualizando sala com ID {room_id}")
    print("Dados recebidos:", room)
    return room.model_dump(), 202
  except ValidationError as e:
    return e.errors(), 400

@app.route("/", methods=["GET"])
def dashboard_view():
  return flask.render_template("dashboard.html")

if __name__ == "__main__":
  app.run(debug=True)