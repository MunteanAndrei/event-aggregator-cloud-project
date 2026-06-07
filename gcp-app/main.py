from datetime import datetime
from typing import Optional, List

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google.cloud import firestore


app = FastAPI(
    title="Event Aggregator GCP App",
    description="App Engine + Firestore version of the Event Aggregator project.",
    version="1.0.0"
)

db = firestore.Client()
EVENTS_COLLECTION = "events"


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    city: str
    location: Optional[str] = None
    category: Optional[str] = None
    event_date: Optional[str] = None
    source_name: str
    source_url: str


class EventResponse(EventCreate):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


def event_doc_to_dict(doc):
    data = doc.to_dict()
    data["id"] = doc.id
    return data


def collect_demo_events():
    return [
        {
            "title": "Tech Conference Timisoara",
            "description": "A technology conference for students and professionals.",
            "city": "Timisoara",
            "location": "Convention Center Timisoara",
            "category": "Technology",
            "event_date": "2026-07-10T10:00:00",
            "source_name": "Demo Scraper",
            "source_url": "https://example.com/events/tech-conference-timisoara"
        },
        {
            "title": "Food Festival Cluj",
            "description": "Outdoor food festival with local restaurants.",
            "city": "Cluj-Napoca",
            "location": "Central Park",
            "category": "Food",
            "event_date": "2026-07-15T18:00:00",
            "source_name": "Demo Scraper",
            "source_url": "https://example.com/events/food-festival-cluj"
        },
        {
            "title": "Theatre Night Bucuresti",
            "description": "Evening theatre performance in Bucharest.",
            "city": "Bucuresti",
            "location": "National Theatre",
            "category": "Theatre",
            "event_date": "2026-07-20T20:00:00",
            "source_name": "Demo Scraper",
            "source_url": "https://example.com/events/theatre-night-bucuresti"
        },
        {
            "title": "Startup Meetup Iasi",
            "description": "Networking event for startup founders and students.",
            "city": "Iasi",
            "location": "Innovation Hub Iasi",
            "category": "Business",
            "event_date": "2026-08-05T17:30:00",
            "source_name": "Demo Scraper",
            "source_url": "https://example.com/events/startup-meetup-iasi"
        }
    ]


@app.get("/api/health")
def health_check():
    return {
        "status": "running",
        "service": "Event Aggregator App Engine version"
    }


@app.get("/events", response_model=List[EventResponse])
def get_events(
    city: Optional[str] = None,
    category: Optional[str] = None,
    source_name: Optional[str] = None
):
    docs = db.collection(EVENTS_COLLECTION).stream()
    events = [event_doc_to_dict(doc) for doc in docs]

    if city:
        events = [
            event for event in events
            if city.lower() in event.get("city", "").lower()
        ]

    if category:
        events = [
            event for event in events
            if category.lower() in event.get("category", "").lower()
        ]

    if source_name:
        events = [
            event for event in events
            if source_name.lower() in event.get("source_name", "").lower()
        ]

    events.sort(key=lambda event: event.get("event_date") or "")

    return events


@app.post("/events", response_model=EventResponse)
def create_event(event: EventCreate):
    existing_events = (
        db.collection(EVENTS_COLLECTION)
        .where("source_url", "==", event.source_url)
        .limit(1)
        .stream()
    )

    if any(existing_events):
        raise HTTPException(
            status_code=400,
            detail="Event with this source_url already exists"
        )

    now = datetime.utcnow().isoformat()

    event_data = event.model_dump()
    event_data["created_at"] = now
    event_data["updated_at"] = now

    doc_ref = db.collection(EVENTS_COLLECTION).document()
    doc_ref.set(event_data)

    event_data["id"] = doc_ref.id
    return event_data


@app.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: str):
    doc_ref = db.collection(EVENTS_COLLECTION).document(event_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Event not found")

    return event_doc_to_dict(doc)


@app.delete("/events/{event_id}")
def delete_event(event_id: str):
    doc_ref = db.collection(EVENTS_COLLECTION).document(event_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Event not found")

    doc_ref.delete()

    return {"message": "Event deleted successfully"}


@app.get("/scrape/status")
def scrape_status():
    return {
        "status": "ready",
        "message": "Scraper service is available"
    }


@app.get("/scrape/preview")
def preview_scraped_events():
    collected_events = collect_demo_events()

    return {
        "total_events": len(collected_events),
        "events": collected_events
    }


@app.post("/scrape")
def scrape_events():
    collected_events = collect_demo_events()

    inserted = 0
    skipped = 0

    for event_data in collected_events:
        existing_events = (
            db.collection(EVENTS_COLLECTION)
            .where("source_url", "==", event_data["source_url"])
            .limit(1)
            .stream()
        )

        if any(existing_events):
            skipped += 1
            continue

        now = datetime.utcnow().isoformat()
        event_data["created_at"] = now
        event_data["updated_at"] = now

        db.collection(EVENTS_COLLECTION).document().set(event_data)
        inserted += 1

    return {
        "message": "Scraping completed",
        "total_collected": len(collected_events),
        "inserted_events": inserted,
        "skipped_duplicates": skipped
    }


app.mount("/", StaticFiles(directory="static", html=True), name="static")