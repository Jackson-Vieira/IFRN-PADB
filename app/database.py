# imports database here

ROOM_TABLE = """
    CREATE TABLE IF NOT EXISTS ROOMS (
        id serial PRIMARY KEY,
        name varchar(50) NOT NULL,
        description varchar(100) NOT NULL,
        enable boolean NOT NULL,
        start_date DATETIME NOT NULL,
        end_date DATETIME NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP 
    )
"""

MESSAGE_TABLE = """
    CREATE TABLE IF NOT EXISTS MESSAGES (
        id serial PRIMARY KEY,
        message varchar(100) NOT NULL,
        room_id integer NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    )
"""


# create connection and cursor here