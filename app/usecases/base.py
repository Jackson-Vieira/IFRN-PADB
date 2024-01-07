class BaseRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def execute_query(self, query, params=None):
        cursor = self.db_connection.cursor()
        cursor.execute(query, params)
        return cursor

    def fetch_one(self, cursor):
        data = cursor.fetchone()
        cursor.close()
        return data

    def fetch_all(self, cursor):
        data = cursor.fetchall()
        cursor.close()
        return data