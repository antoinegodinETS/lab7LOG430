from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Text

Base = declarative_base()

class Evenement(Base):
    __tablename__ = "evenements"
    id = Column(String, primary_key=True)         # UUID
    type = Column(String)
    source = Column(String)
    timestamp = Column(DateTime)
    payload = Column(Text)
