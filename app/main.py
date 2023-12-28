import flask
import psycopg2

from flask import request
from pydantic import BaseModel, ValidationError
from decouple import config

from database import ROOM_TABLE, MESSAGE_TABLE

DATABASE_URL = config("DATABASE_URL")

app = flask.Flask(__name__)

def connect_db():
    return psycopg2.connect(DATABASE_URL)

def test_db_connection():
    # run script to test connection with the db 
    ...

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
    room = RoomCreate(**request.get_json())

    with connect_db() as conn:
      with conn.cursor() as cur:
        cur.execute(INSERT_ROOM_SQL, **room.model_dump())

    return room.model_dump(), 202

  except ValidationError as e:
    return e.errors(), 400
  except Exception as e:
    return e, 500
    
@app.route("/api/v1/rooms/<room_id>", methods=["DELETE"])
def remover_room(room_id):

  # TODO: check if room exists first
  with connect_db() as conn:
    with conn.cursor() as cur:
      cur.execute(DELETE_ROOM_SQL, {"id": room_id})
      conn.commit()

  return f"Remover sala com ID {room_id}", 200

@app.route("/api/v1/rooms/<room_id>", methods=["PUT"]) # CASO PRATICO: QUAL A DIFERENCA ENTRE PUT E PATCH?
def update_room(room_id):
  try:
    room = RoomCreate(**request.get_json())
    room_dict = room.model_dump()

    # TODO: check if room exists first
    with connect_db() as conn:
      with conn.cursor() as cur:
        cur.execute(UPDATE_ROOM_SQL, {"id": room_id, **room_dict()})
        conn.commit()

    return room_dict, 202

  except ValidationError as e:
    return e.errors(), 400
  except Exception as e:
    return e, 500

@app.route("/", methods=["GET"])
def dashboard_view():
  return flask.render_template("dashboard.html")

if __name__ == "__main__":
  # test_db_connection()

  with connect_db() as conn:
    with conn.cursor() as cur:
      cur.execute(ROOM_TABLE)
      cur.execute(MESSAGE_TABLE)
      conn.commit()
  
  # TODO: only start the server if db connection is ok
  app.run(debug=True)