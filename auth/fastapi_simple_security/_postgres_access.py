import os 
import threading
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from fastapi import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_403_FORBIDDEN,
)

import psycopg2 as pg
from psycopg2 import Error



class PostgresAccess:
    """Class handling Remote Postgres connection and writes. Alter _config.py if migrating database to new location"""

    # TODO This should not be a class, a fully functional approach is better

    def __init__(self):
        
        try:
            # Connect to an existing database
            

            URI = os.environ["URI"]
            connection = pg.connect(URI, sslmode='require')

            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Print PostgreSQL details
            print("PostgreSQL server information")
            print(connection.get_dsn_parameters(), "\n")
            # Executing a SQL query
            cursor.execute("SELECT version();")
            # Fetch result
            record = cursor.fetchone()
            print("You are connected to - ", record, "\n")

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL:", error)

        try:
            self.expiration_limit = int(
                os.environ["FAST_API_SIMPLE_SECURITY_AUTOMATIC_EXPIRATION"]
            )
        except KeyError:
            self.expiration_limit = 15

        self.init_db()

    def init_db(self):
        with pg.connect(URI, sslmode='require') as connection:
            c = connection.cursor()
            # Create database
            c.execute(
                """
        CREATE TABLE IF NOT EXISTS user_database (
            api_key TEXT PRIMARY KEY,
            is_active INTEGER,
            never_expire INTEGER,
            expiration_date TEXT,
            latest_query_date TEXT,
            total_queries INTEGER)
        """
            )
            connection.commit()
            # Migration: Add api key username
            try:
                c.execute("ALTER TABLE user_database RENAME COLUMN name TO username")
                c.execute("ALTER TABLE user_database ADD COLUMN email TEXT")
                c.execute("ALTER TABLE user_database ADD COLUMN password TEXT"
                )
                c.execute("ALTER TABLE user_database ADD COLUMN username TEXT")
                connection.commit()
            except pg.Error:
                pass  # Column already exist
            
    def create_key(self, username, email, password, never_expire) -> str:
        api_key = str(uuid.uuid4())

        with pg.connect(URI, sslmode='require') as connection:
            c = connection.cursor()
            c.execute(
                """SELECT username, email
                   FROM user_database
                   WHERE username=%s OR email=%s""",
                (username, email),
            )
            result = c.fetchone()
            if result:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="This user already exists in the database. Please choose another userusername or password.",
                )
            else:
                c.execute(
                    """
                    INSERT INTO user_database
                    (api_key, is_active, never_expire, expiration_date, \
                        latest_query_date, total_queries, username, email, password)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        api_key,
                        1,
                        1 if never_expire else 0,
                        (
                            datetime.utcnow() + timedelta(days=self.expiration_limit)
                        ).isoformat(timespec="seconds"),
                        None,
                        0,
                        username,
                        email,
                        password,
                    ),
                )
                connection.commit()

        return api_key

    def renew_key(self, api_key: str, new_expiration_date: str) -> Optional[str]:
        with pg.connect(URI, sslmode='require') as connection:
            c = connection.cursor()

            # We run the query like check_key but will use the response differently
            c.execute(
                """
            SELECT is_active, total_queries, expiration_date, never_expire
            FROM user_database
            WHERE api_key = %s""",
                (api_key,),
            )

            response = c.fetchone()

            # API key not found
            if not response:
                raise HTTPException(
                    status_code=HTTP_404_NOT_FOUND, detail="API key not found"
                )

            response_lines = []

            # Previously revoked key. Issue a text warning and reactivate it.
            if response[0] == 0:
                response_lines.append(
                    "This API key was revoked and has been reactivated."
                )

            # Without an expiration date, we set it here
            if not new_expiration_date:
                parsed_expiration_date = (
                    datetime.utcnow() + timedelta(days=self.expiration_limit)
                ).isoformat(timespec="seconds")

            else:
                try:
                    # We parse and re-write to the right timespec
                    parsed_expiration_date = datetime.fromisoformat(
                        new_expiration_date
                    ).isoformat(timespec="seconds")
                except ValueError as exc:
                    raise HTTPException(
                        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="The expiration date could not be parsed. \
                            Please use ISO 8601.",
                    ) from exc

            c.execute(
                """
            UPDATE user_database
            SET expiration_date = %s, is_active = 1
            WHERE api_key = %s
            """,
                (
                    parsed_expiration_date,
                    api_key,
                ),
            )

            connection.commit()

            response_lines.append(
                f"The new expiration date for the API key is {parsed_expiration_date}"
            )

            return " ".join(response_lines)

    def revoke_key(self, api_key: str):
        """
        Revokes an API key

        Args:
            api_key: the API key to revoke
        """
        with pg.connect(URI, sslmode='require') as connection:
            c = connection.cursor()

            c.execute(
                """
            UPDATE user_database
            SET is_active = 0
            WHERE api_key = %s
            """,
                (api_key,),
            )

            connection.commit()

    def check_key(self, api_key: str) -> bool:
        """
        Checks if an API key is valid

        Args:
             api_key: the API key to validate
        """

        with pg.connect(URI, sslmode='require') as connection:
            c = connection.cursor()

            c.execute(
                """
            SELECT is_active, total_queries, expiration_date, never_expire
            FROM user_database
            WHERE api_key = %s""",
                (api_key,),
            )

            response = c.fetchone()

            if (
                # Cannot fetch a row
                not response
                # Inactive
                or response[0] != 1
                # Expired key
                or (
                    (not response[3])
                    and (datetime.fromisoformat(response[2]) < datetime.utcnow())
                )
            ):
                # The key is not valid
                return False
            else:
                # The key is valid

                # We run the logging in a separate thread as writing takes some time
                threading.Thread(
                    target=self._update_usage,
                    args=(
                        api_key,
                        response[1],
                    ),
                ).start()

                # We return directly
                return True

    def _update_usage(self, api_key: str, usage_count: int):
        with pg.connect(URI, sslmode='require') as connection:
            c = connection.cursor()

            # If we get there, this means it’s an active API key that’s in the database.\
            #   We update the table.
            c.execute(
                """
            UPDATE user_database
            SET total_queries = %s, latest_query_date = %s
            WHERE api_key = %s
            """,
                (
                    usage_count + 1,
                    datetime.utcnow().isoformat(timespec="seconds"),
                    api_key,
                ),
            )

            connection.commit()

    def get_usage_stats(self) -> List[Tuple[str, bool, bool, str, str, int]]:
        """
        Returns usage stats for all API keys

        Returns:
            a list of tuples with values being api_key, is_active, expiration_date, \
                latest_query_date, and total_queries
        """
        with pg.connect(URI, sslmode='require') as connection:
            c = connection.cursor()

            c.execute(
                """
            SELECT api_key, is_active, never_expire, expiration_date, \
                latest_query_date, total_queries, username, email
            FROM user_database
            ORDER BY latest_query_date DESC
            """,
            )

            response = c.fetchall()

        return response


postgres_access = PostgresAccess()