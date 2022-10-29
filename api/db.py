"""Interaction with SQLite database.
"""
import os
import sqlite3
import threading
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Tuple


class SQLiteAccess:
    """Class handling SQLite connection and writes"""

    # TODO This should not be a class, a fully functional approach is better

    def __init__(self):
        try:
            self.db_location = os.environ["FASTAPI_SIMPLE_SECURITY_DB_LOCATION"]
        except KeyError:
            self.db_location = "sqlite.db"

        try:
            self.expiration_limit = int(
                os.environ["FAST_API_SIMPLE_SECURITY_AUTOMATIC_EXPIRATION"]
            )
        except KeyError:
            self.expiration_limit = 15

        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_location) as connection:
            c = connection.cursor()
            # Create database
            c.execute(
                """
        CREATE TABLE IF NOT EXISTS fastapi_simple_security (
            api_key TEXT PRIMARY KEY,
            is_active INTEGER,
            never_expire INTEGER,
            expiration_date TEXT,
            latest_query_date TEXT,
            total_queries INTEGER)
        """
            )
            connection.commit()
            # Migration: Add api key name
            try:
                c.execute("ALTER TABLE fastapi_simple_security ADD COLUMN email TEXT")
                c.execute("ALTER TABLE fastapi_simple_security ADD COLUMN password TEXT")
                connection.commit()
            except sqlite3.OperationalError:
                print(str(sqlite3.OperationalError))
                # Column already exist
            
update = SQLiteAccess()
update.init_db