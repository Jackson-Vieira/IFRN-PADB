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

@pytest.fixture
def create_room_data():
    return {
        "name": "Room 1",
        "description": "Room 1 Description",
        "enable": True,
        "start_date": datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S"),
        "end_date": datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S")
    }

@pytest.fixture
def create_room(room_usecases ,create_room_data):
    rid = room_usecases.create_room(create_room_data)
    yield rid
    room_usecases.delete_room(rid)

def test_list_rooms(room_usecases):
    rooms = room_usecases.get_all_rooms()
    assert len(rooms) == 0

def test_create_room(room_usecases, create_room_data):
    rooms = room_usecases.get_all_rooms()
    assert len(rooms) == 0

    rid = room_usecases.create_room(create_room_data)
    assert isinstance(rid, int) is True

    rooms = room_usecases.get_all_rooms()
    assert len(rooms) == 1

    room_usecases.delete_room(rid)

def test_update_room(room_usecases, create_room_data):
    rooms = room_usecases.get_all_rooms()
    assert len(rooms) == 0

    rid = room_usecases.create_room(create_room_data)
    assert isinstance(rid, int) is True

    rooms = room_usecases.get_all_rooms()
    assert len(rooms) == 1

    update_data = {
        **create_room_data,
        "enable": False,
    }

    room_usecases.update_room(rid, update_data)

    room = room_usecases.get_room_by_id(rid)
    
    assert room[3] is False

    room_usecases.delete_room(rid)

def test_search(room_usecases, create_room):
    rooms = room_usecases.search("Ro")
    assert len(rooms) == 1