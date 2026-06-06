from typing import Optional, List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Event
from schemas import EventCreate, EventResponse

from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Event API Service",
    description="REST API for listing and filtering public events.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Event API Service is running",
        "docs": "/docs"
    }


@app.post("/events", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    existing_event = db.query(Event).filter(Event.source_url == event.source_url).first()

    if existing_event:
        raise HTTPException(status_code=400, detail="Event with this source_url already exists")

    db_event = Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event


@app.get("/events", response_model=List[EventResponse])
def get_events(
    city: Optional[str] = None,
    category: Optional[str] = None,
    source_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Event)

    if city:
        query = query.filter(Event.city.ilike(f"%{city}%"))

    if category:
        query = query.filter(Event.category.ilike(f"%{category}%"))

    if source_name:
        query = query.filter(Event.source_name.ilike(f"%{source_name}%"))

    return query.order_by(Event.event_date.asc()).all()


@app.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


@app.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()

    return {"message": "Event deleted successfully"}