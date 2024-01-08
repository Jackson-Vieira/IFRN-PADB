import flask
import psycopg2

from flask import request, jsonify
from flask_cors import CORS
from pydantic import BaseModel, ValidationError
from decouple import config

from database import ROOM_TABLE, MESSAGE_TABLE

from usecases.room_usecases import RoomUseCases, RoomRepository

DATABASE_URL = config("DATABASE_URL")

app = flask.Flask(__name__)
CORS(app, origins=["localhost"])


def connect_db():
    return psycopg2.connect(DATABASE_URL)


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

        db_connection = connect_db()

        room_repository = RoomRepository(db_connection)
        room_uc = RoomUseCases(room_repository)
        room_uc.create_room(room_dict)

        db_connection.close()

        return room_dict, 202

    except ValidationError as e:
        return e.errors(), 400
    except Exception as e:
        print(e)


@app.route("/api/v1/rooms", methods=["GET"])
def get_rooms():
    try:
        db_connection = connect_db()

        search = request.args.get("search")

        room_repository = RoomRepository(db_connection)
        room_uc = RoomUseCases(room_repository)

        if search:
            rooms = room_uc.search(query=search)
        else:
            rooms = room_uc.get_all_rooms()

        db_connection.close()

        return jsonify({"data": rooms}), 200

    except Exception as e:
        print(e)
        return "Internal Server Error", 500


@app.route("/api/v1/rooms/<room_id>", methods=["DELETE"])
def remover_room(room_id):
    try:
        db_connection = connect_db()

        room_repository = RoomRepository(db_connection)
        room_uc = RoomUseCases(room_repository)
        room_uc.delete_room(rid=room_id)

        db_connection.close()

    # check if room exists and return a 404 if not

    except Exception as e:
        return "", 500

    return "", 200


@app.route("/api/v1/rooms/<room_id>", methods=["PUT"])
def update_room(room_id):
    try:
        room = RoomCreate(**request.get_json())
        room_dict = room.model_dump()

        db_connection = connect_db()

        room_repository = RoomRepository(db_connection)
        room_uc = RoomUseCases(room_repository)
        room_uc.update_room(room_id, room_dict)

        db_connection.close()

        return "", 200

    except ValidationError as e:
        return e.errors(), 400
    except Exception as e:
        print(e)
        return e, 500


@app.route("/", methods=["GET"])
def dashboard_view():
    try:
        db_connection = connect_db()

        room_repository = RoomRepository(db_connection)
        room_uc = RoomUseCases(room_repository)
        rooms = room_uc.get_all_rooms()

        db_connection.close()

    except Exception as e:
        print(e)
        return "", 500

    return flask.render_template("dashboard.html", rooms=rooms)


if __name__ == "__main__":
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(ROOM_TABLE)
            cur.execute(MESSAGE_TABLE)
            conn.commit()

    app.run(debug=False)
