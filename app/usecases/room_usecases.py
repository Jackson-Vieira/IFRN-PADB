# from pydantic import BaseModel
from .base import BaseRepository
import datetime


class RoomRepository(BaseRepository):
    INSERT_ROOM_SQL = """
        INSERT INTO Rooms (name, description, enable, start_date, end_date)
        VALUES (%(name)s, %(description)s, %(enable)s, %(start_date)s, %(end_date)s)
        RETURNING id
    """

    GET_ROOM_SQL = """
        SELECT id, name, description, enable, start_date, end_date, created_at, updated_at FROM Rooms WHERE id = %(id)s
    """

    GET_ROOMS_SQL = """
        SELECT 
            id, 
            name, 
            description, 
            enable, 
            TO_CHAR(start_date, 'YYYY-MM-DD HH24:MI:SS') AS start_date, 
            TO_CHAR(end_date, 'YYYY-MM-DD HH24:MI:SS') AS end_date 
        FROM Rooms
    """

    DELETE_ROOM_SQL = """
        DELETE FROM Rooms WHERE id = %(id)s
    """

    UPDATE_ROOM_SQL = """
        UPDATE Rooms SET name = %(name)s, description = %(description)s, enable = %(enable)s, start_date = %(start_date)s, end_date = %(end_date)s, updated_at = %(updated_at)s
        WHERE id = %(id)s
    """

    SEARCH_ROOMS_SQL = """
        SELECT 
            id, 
            name, 
            description, 
            enable, 
            TO_CHAR(start_date, 'YYYY-MM-DD HH24:MI:SS') AS start_data, 
            TO_CHAR(end_date, 'YYYY-MM-DD HH24:MI:SS') AS end_date 
        FROM Rooms 
        WHERE name LIKE %(pattern)s
    """

    def create_room(self, data):
        cursor = self.execute_query(self.INSERT_ROOM_SQL, data)
        new_rid = self.fetch_one(cursor)[0]
        self.db_connection.commit()
        return new_rid

    def get_room_by_id(self, rid):
        cursor = self.execute_query(self.GET_ROOM_SQL, {"id": rid})
        return self.fetch_one(cursor)

    def get_rooms(self):
        cursor = self.execute_query(self.GET_ROOMS_SQL)
        return self.fetch_all(cursor)

    def delete_room(self, rid: int):
        cursor = self.execute_query(self.DELETE_ROOM_SQL, {"id": rid})
        self.db_connection.commit()

    def update(self, rid, data):
        cursor = self.execute_query(
            self.UPDATE_ROOM_SQL,
            {"id": rid, "updated_at": datetime.datetime.now(), **data},
        )
        self.db_connection.commit()

    def search(self, query):
        cursor = self.execute_query(self.SEARCH_ROOMS_SQL, {"pattern": f"{query}%"})
        return self.fetch_all(cursor)


class RoomUseCases:
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

    def create_room(self, data: dict):
        rid = self.room_repository.create_room(data)
        return rid

    def get_room_by_id(self, rid: int):
        return self.room_repository.get_room_by_id(rid)

    def delete_room(self, rid: int):
        self.room_repository.delete_room(rid)

    def update_room(self, rid: int, data: dict):
        self.room_repository.update(rid, data)

    def get_all_rooms(self) -> []:
        return self.room_repository.get_rooms()

    def search(self, query) -> []:
        return self.room_repository.search(query)
