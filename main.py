from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from models import Event
from database import SessionLocal, engine, Base

# Инициализация базы данных
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic-схемы для валидации данных
from pydantic import BaseModel

class EventBase(BaseModel):
    name: str
    event_date: datetime
    event_type: str | None = None
    budget: float | None = None

class EventCreate(EventBase):
    pass

class EventRead(EventBase):
    event_id: int

    class Config:
        orm_mode = True

# Создание нового мероприятия
@app.post("/events/", response_model=EventRead)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

# Получение списка всех мероприятий
@app.get("/events/", response_model=List[EventRead])
def read_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events

# Получение одного мероприятия по ID
@app.get("/events/{event_id}", response_model=EventRead)
def read_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# Обновление мероприятия
@app.put("/events/{event_id}", response_model=EventRead)
def update_event(event_id: int, updated_event: EventCreate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    for key, value in updated_event.dict().items():
        setattr(event, key, value)
    db.commit()
    db.refresh(event)
    return event

# Удаление мероприятия
@app.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(event)
    db.commit()
    return {"message": "Event deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)