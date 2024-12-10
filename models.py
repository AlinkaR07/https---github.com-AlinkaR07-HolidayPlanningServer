from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from database import Base

# ---- Модель для мероприятий ----
class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    event_date = Column(DateTime, nullable=False)
    event_type = Column(String)
    budget = Column(Numeric(12, 2))

    # Связь с подрядчиками
    contractors = relationship("Contractor", back_populates="event")


# ---- Модель для категорий подрядчиков ----
class ContractorCategory(Base):
    __tablename__ = "contractor_categories"  # Добавьте эту строку

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, nullable=False)

    # Связь с подрядчиками
    contractors = relationship("Contractor", back_populates="category")


# ---- Модель для подрядчиков ----
class Contractor(Base):
    __tablename__ = "contractors"

    contractor_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    description = Column(String)
    phone_number = Column(String)
    service_cost = Column(Float)

    # Внешние ключи
    category_id = Column(Integer, ForeignKey("contractor_categories.category_id"))
    event_id = Column(Integer, ForeignKey("events.event_id"))

    # Связи
    category = relationship("ContractorCategory", back_populates="contractors")
    event = relationship("Event", back_populates="contractors")


# ---- Модель для гостей ----
class Guest(Base):
    __tablename__ = "guests"

    guest_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    guest_type = Column(String)
    category = Column(String)
    comment = Column(String)
    status = Column(String)
    phone_number = Column(String)
