from sqlalchemy import create_engine
from models.base import Base
from sqlalchemy.exc import SQLAlchemyError

def create_tables(db_url):
    try:
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        print("DEBUG: Tables created")
    except SQLAlchemyError as e:
        print("ERROR: Error during tables creation: %s", e)

def drop_tables(db_url):
    try:
        engine = create_engine(db_url)
        Base.metadata.drop_all(engine)
        print("DEBUG: Tables dropped")
    except SQLAlchemyError as e:
        print("ERROR: Error during tables dropping: %s", e)