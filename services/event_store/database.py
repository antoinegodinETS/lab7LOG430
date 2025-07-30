from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://event_user:password@db_event_store:5432/event_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
