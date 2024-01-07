import pytest
import psycopg2
from decouple import config

import datetime

from app.usecases.room_usecases import RoomUseCases, RoomRepository

DATABASE_URL = config("DATABASE_URL")

@pytest.fixture
def db_connection():
    connection = psycopg2.connect(DATABASE_URL)
    yield connection
    connection.close()

@pytest.fixture
def room_usecases(db_connection):
    room_repository = RoomRepository(db_connection)
    return RoomUseCases(room_repository)

def test_list_rooms(room_usecases):
    rooms = room_usecases.get_all_rooms()
    ...

def test_create_room(room_usecases):
    rid = room_usecases.create_room({
        "name": "Room 1",
        "description": "Room 1 Description",
        "enable": True,
        "start_date": datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S"),
        "end_date": datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S")
    })

    assert isinstance(rid, int) is True

    room_usecases.delete_room(rid)

def test_search(room_usecases):
    rid = room_usecases.create_room({
        "name": "Room 1",
        "description": "Room 1 Description",
        "enable": True,
        "start_date": datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S"),
        "end_date": datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S")
    })

    rooms = room_usecases.search("Ro")

    assert len(rooms) == 1

    room_usecases.delete_room(rid)