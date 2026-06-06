# API Documentation

## 1. Overview

The application exposes two separate REST APIs:

1. Event API Service
2. Scraper Service

The Event API Service is responsible for reading, creating, filtering and deleting events.

The Scraper Service is responsible for collecting event data and inserting it into the database.

---

## 2. Event API Service

Base URL for local development:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

### 2.1 Root Endpoint

```http
GET /
```

Description:

Returns a simple message confirming that the Event API Service is running.

Example response:

```json
{
  "message": "Event API Service is running",
  "docs": "/docs"
}
```

---

### 2.2 Get Events

```http
GET /events
```

Description:

Returns all events from the database. The endpoint also supports optional filters.

Optional query parameters:

```text
city
category
source_name
```

Example requests:

```http
GET /events
GET /events?city=Timisoara
GET /events?category=Technology
GET /events?source_name=Demo Scraper
```

Example response:

```json
[
  {
    "title": "Tech Conference Timisoara",
    "description": "A technology conference for students and professionals.",
    "city": "Timisoara",
    "location": "Convention Center Timisoara",
    "category": "Technology",
    "event_date": "2026-07-10T10:00:00",
    "source_name": "Demo Scraper",
    "source_url": "https://example.com/events/tech-conference-timisoara",
    "id": 2,
    "created_at": "2026-06-07T10:00:00",
    "updated_at": "2026-06-07T10:00:00"
  }
]
```

---

### 2.3 Create Event

```http
POST /events
```

Description:

Creates a new event in the database.

The `source_url` field must be unique. If another event already exists with the same `source_url`, the API returns an error.

Example request body:

```json
{
  "title": "Concert Rock in Timisoara",
  "description": "A public rock concert in the city center.",
  "city": "Timisoara",
  "location": "Piata Unirii",
  "category": "Music",
  "event_date": "2026-06-20T19:00:00",
  "source_name": "Manual Test",
  "source_url": "https://example.com/events/concert-rock-timisoara"
}
```

Example response:

```json
{
  "title": "Concert Rock in Timisoara",
  "description": "A public rock concert in the city center.",
  "city": "Timisoara",
  "location": "Piata Unirii",
  "category": "Music",
  "event_date": "2026-06-20T19:00:00",
  "source_name": "Manual Test",
  "source_url": "https://example.com/events/concert-rock-timisoara",
  "id": 1,
  "created_at": "2026-06-07T10:00:00",
  "updated_at": "2026-06-07T10:00:00"
}
```

Duplicate event response:

```json
{
  "detail": "Event with this source_url already exists"
}
```

---

### 2.4 Get Event by ID

```http
GET /events/{event_id}
```

Description:

Returns one event based on its ID.

Example request:

```http
GET /events/1
```

Example not found response:

```json
{
  "detail": "Event not found"
}
```

---

### 2.5 Delete Event

```http
DELETE /events/{event_id}
```

Description:

Deletes an event based on its ID.

Example request:

```http
DELETE /events/1
```

Example response:

```json
{
  "message": "Event deleted successfully"
}
```

---

## 3. Scraper Service

Base URL for local development:

```text
http://127.0.0.1:8001
```

Swagger documentation:

```text
http://127.0.0.1:8001/docs
```

---

### 3.1 Root Endpoint

```http
GET /
```

Description:

Returns a simple message confirming that the Scraper Service is running.

Example response:

```json
{
  "message": "Scraper Service is running",
  "docs": "/docs"
}
```

---

### 3.2 Scraper Status

```http
GET /scrape/status
```

Description:

Returns the current availability status of the scraper service.

Example response:

```json
{
  "status": "ready",
  "message": "Scraper service is available"
}
```

---

### 3.3 Preview Scraped Events

```http
GET /scrape/preview
```

Description:

Returns the events collected by the scraper without inserting them into the database.

This endpoint is useful for testing and demonstrating the scraper logic.

Example response:

```json
{
  "total_events": 4,
  "events": [
    {
      "title": "Tech Conference Timisoara",
      "description": "A technology conference for students and professionals.",
      "city": "Timisoara",
      "location": "Convention Center Timisoara",
      "category": "Technology",
      "event_date": "2026-07-10T10:00:00",
      "source_name": "Demo Scraper",
      "source_url": "https://example.com/events/tech-conference-timisoara"
    }
  ]
}
```

---

### 3.4 Run Scraper

```http
POST /scrape
```

Description:

Runs the scraper process and inserts collected events into the PostgreSQL database.

If an event already exists, it is skipped based on the unique `source_url`.

Example response:

```json
{
  "message": "Scraping completed",
  "total_collected": 4,
  "inserted_events": 1,
  "skipped_duplicates": 3
}
```

---

## 4. API Separation

The project contains two separate API interfaces:

### Event API

Used by the frontend to retrieve and filter events.

Main responsibility:

```text
Read and manage event data
```

### Scraper API

Used to collect events from external sources and save them to the database.

Main responsibility:

```text
Collect and insert event data
```

This separation follows the microservices approach, where each service has a clear and independent responsibility.