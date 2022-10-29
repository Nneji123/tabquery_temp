from sqlalchemy import *
from _config import host, port, database, user, passwordconn_str = f"postgresql://{user}:{password}@{host}/{database}"
engine = create_engine(conn_str)
connection = engine.connect()
metadata = MetaData()userbase = Table('userbase', metadata,
   Column('api_key', String, primary_key=True),
   Column('is_active', Integer, nullable=False),
   Column('never_expire', Integer, nullable=False),
   Column('expiration_date', String, nullable=False),
   Column('latest_query_date', String, nullable=False),
   Column('total_queries', Integer, nullable=False),
   Column('name', String, nullable=False),
   Column('email', String, nullable=False),
   Column('password', String, nullable=False),
)metadata.create_all(engine)


query = insert(userbase).values(api_key="f69ef4c-616b-476a-9e03-7f97ed88a960", is_active=0, never_expire=1, expiration_date="2022-11-13T07:04:45", latest_query_date="")
ResultProxy = connection.execute(query)