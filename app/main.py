import flask
import psycopg2

from flask import request
from flask_cors import CORS
from pydantic import BaseModel, ValidationError
from decouple import config

import datetime

from database import ROOM_TABLE, MESSAGE_TABLE

DATABASE_URL = config("DATABASE_URL")

app = flask.Flask(__name__)
CORS(app, origins=["localhost"])

def connect_db():
    return psycopg2.connect(DATABASE_URL)

# def test_db_connection():
#     # run script to test connection with the db 
#     ...

class RoomBase(BaseModel):
  name: str
  description: str
  enable: bool
  start_date: str
  end_date: str

class RoomCreate(RoomBase):
  ...

class Room(RoomBase):
  id: int

@app.route("/api/v1/rooms", methods=["POST"])
def create_room():
  try:
    room = RoomCreate(**request.get_json())
    room_dict = room.model_dump()

    with connect_db() as conn:
      with conn.cursor() as cur:
        cur.execute(INSERT_ROOM_SQL, room_dict)

    return room_dict, 202

  except ValidationError as e:
    return e.errors(), 400
  except Exception as e:
    print(e)
    return "Internal Server Error", 500
    
@app.route("/api/v1/rooms/<room_id>", methods=["DELETE"])
def remover_room(room_id):

  # TODO: check if room exists first
  with connect_db() as conn:
    with conn.cursor() as cur:
      cur.execute(DELETE_ROOM_SQL, {"id": room_id})
      conn.commit()

  return "", 200

@app.route("/api/v1/rooms/<room_id>", methods=["PUT"]) # CASO PRATICO: QUAL A DIFERENCA ENTRE PUT E PATCH?
def update_room(room_id):
  try:
    room = RoomCreate(**request.get_json())
    room_dict = room.model_dump()
    room_dict["updated_at"] = datetime.datetime.now()

    # TODO: check if room exists first
    with connect_db() as conn:
      with conn.cursor() as cur:
        cur.execute(UPDATE_ROOM_SQL, {"id": room_id, **room_dict})
        conn.commit()

    return "", 200

  except ValidationError as e:
    return e.errors(), 400
  except Exception as e:
    print(e)
    return e, 500

@app.route("/", methods=["GET"])
def dashboard_view():

  rooms = []
  with connect_db() as conn:
    with conn.cursor() as cur:
      cur.execute(GET_ROOMS_SQL)
      rooms = cur.fetchall()

  return flask.render_template("dashboard.html", rooms=rooms)

if __name__ == "__main__":
  # test_db_connection()

  with connect_db() as conn:
    with conn.cursor() as cur:
      cur.execute(ROOM_TABLE)
      cur.execute(MESSAGE_TABLE)
      conn.commit()
  
  # TODO: only start the server if db connection is ok
  app.run(debug=True)