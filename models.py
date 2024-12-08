from sqlalchemy import Column, Integer, String, Numeric, DateTime
from database import Base

class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    event_date = Column(DateTime, nullable=False)
    event_type = Column(String)
    budget = Column(Numeric(12, 2))