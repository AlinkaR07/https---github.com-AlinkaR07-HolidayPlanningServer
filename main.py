from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from models import Event, Contractor, ContractorCategory, Guest
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
from datetime import datetime
from typing import Optional


# --- Мероприятия ---
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


# --- Пользователи ---
class UserBase(BaseModel):
    full_name: str
    username: str
    password: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    user_id: int

    class Config:
        from_attributes = True


# --- Подрядчики ---
class ContractorBase(BaseModel):
    category_id: int
    name: str
    status: str
    event_id: int
    description: Optional[str] = None
    phone_number: Optional[str] = None
    service_cost: float

class ContractorCreate(ContractorBase):
    pass

class ContractorRead(ContractorBase):
    contractor_id: int

    class Config:
        from_attributes = True


# --- Гости ---
class GuestBase(BaseModel):
    full_name: str
    guest_type: str
    category: str
    comment: Optional[str] = None
    status: str
    phone_number: str

class GuestCreate(GuestBase):
    pass

class GuestRead(GuestBase):
    guest_id: int

    class Config:
        from_attributes = True


class ContractorCategoryBase(BaseModel):
    category_name: str


class ContractorCategoryCreate(ContractorCategoryBase):
    pass


class ContractorCategoryRead(ContractorCategoryBase):
    category_id: int

    class Config:
        from_attributes = True


# ---- CRUD для мероприятий ----

@app.post("/events/", response_model=EventRead)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/events/", response_model=List[EventRead])
def read_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events

@app.get("/events/{event_id}", response_model=EventRead)
def read_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

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


# ---- CRUD для категорий подрядчиков ----

@app.post("/contractor-categories/", response_model=ContractorCategoryRead)
def create_contractor_category(category: ContractorCategoryCreate, db: Session = Depends(get_db)):
    db_category = ContractorCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@app.get("/contractor-categories/", response_model=List[ContractorCategoryRead])
def read_contractor_categories(db: Session = Depends(get_db)):
    return db.query(ContractorCategory).all()


@app.get("/contractor-categories/{category_id}", response_model=ContractorCategoryRead)
def read_contractor_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(ContractorCategory).filter(ContractorCategory.category_id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# ---- CRUD для подрядчиков ----

@app.post("/contractors/", response_model=ContractorRead)
def create_contractor(contractor: ContractorCreate, db: Session = Depends(get_db)):
    db_contractor = Contractor(**contractor.dict())
    db.add(db_contractor)
    db.commit()
    db.refresh(db_contractor)
    return db_contractor

@app.get("/contractors/", response_model=List[ContractorRead])
def read_contractors(db: Session = Depends(get_db)):
    return db.query(Contractor).all()

@app.get("/contractors/{contractor_id}", response_model=ContractorRead)
def read_contractor(contractor_id: int, db: Session = Depends(get_db)):
    contractor = db.query(Contractor).filter(Contractor.contractor_id == contractor_id).first()
    if contractor is None:
        raise HTTPException(status_code=404, detail="Contractor not found")
    return contractor

@app.put("/contractors/{contractor_id}", response_model=ContractorRead)
def update_contractor(contractor_id: int, updated_contractor: ContractorCreate, db: Session = Depends(get_db)):
    contractor = db.query(Contractor).filter(Contractor.contractor_id == contractor_id).first()
    if contractor is None:
        raise HTTPException(status_code=404, detail="Contractor not found")
    for key, value in updated_contractor.dict().items():
        setattr(contractor, key, value)
    db.commit()
    db.refresh(contractor)
    return contractor

@app.delete("/contractors/{contractor_id}")
def delete_contractor(contractor_id: int, db: Session = Depends(get_db)):
    contractor = db.query(Contractor).filter(Contractor.contractor_id == contractor_id).first()
    if contractor is None:
        raise HTTPException(status_code=404, detail="Contractor not found")
    db.delete(contractor)
    db.commit()
    return {"message": "Contractor deleted successfully"}


# ---- CRUD для гостей ----

@app.post("/guests/", response_model=GuestRead)
def create_guest(guest: GuestCreate, db: Session = Depends(get_db)):
    db_guest = Guest(**guest.dict())
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    return db_guest


@app.get("/guests/", response_model=List[GuestRead])
def read_guests(db: Session = Depends(get_db)):
    return db.query(Guest).all()


@app.get("/guests/{guest_id}", response_model=GuestRead)
def read_guest(guest_id: int, db: Session = Depends(get_db)):
    guest = db.query(Guest).filter(Guest.guest_id == guest_id).first()
    if guest is None:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest