from sqlalchemy import create_engine # this function starts the engine to connect the postgres with fastapi 
from sqlalchemy.orm import sessionmaker # this function starts the session to operate operation on database
from sqlalchemy.ext.declarative import declarative_base # this function converts the python class to the database table

POSTGRESQL_URL = 'postgresql;//postgres:admin@localhost:5432/project2'# this is the postgesql url through which the database and 

engine = create_engine(POSTGRESQL_URL)

Sessionlocal = sessionmaker(autocommit = False , autoflush = False , bind = engine)

base = declarative_base()

