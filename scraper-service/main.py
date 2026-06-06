from datetime import datetime
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.middleware.cors import CORSMiddleware
from scraper import collect_events

from database import Base, engine, get_db
from models import Event

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Scraper Service",
    description="Service responsible for collecting public events from web sources.",
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
        "message": "Scraper Service is running",
        "docs": "/docs"
    }


@app.get("/scrape/status")
def scrape_status():
    return {
        "status": "ready",
        "message": "Scraper service is available"
    }

@app.get("/scrape/preview")
def preview_scraped_events():
    collected_events = collect_events()

    return {
        "total_events": len(collected_events),
        "events": collected_events
    }

@app.post("/scrape")
def scrape_events(db: Session = Depends(get_db)):
    collected_events = collect_events()

    inserted = 0
    skipped = 0

    for event_data in collected_events:
        event = Event(**event_data)
        db.add(event)

        try:
            db.commit()
            inserted += 1
        except IntegrityError:
            db.rollback()
            skipped += 1

    return {
        "message": "Scraping completed",
        "total_collected": len(collected_events),
        "inserted_events": inserted,
        "skipped_duplicates": skipped
    }