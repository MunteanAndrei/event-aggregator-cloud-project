# Event Aggregator - Cloud Computing Project

## 1. Project Overview

Event Aggregator is a web application developed using a microservices architecture. The application collects public event information, stores it in a PostgreSQL database, and exposes REST APIs for listing and filtering events.

The project follows the Red Pill approach, where the application source code is developed from scratch.

Users can view events through a web interface and filter them by city or category. The scraper service can be triggered manually from the frontend to collect events.

## 2. Main Features

- Display public events in a web interface
- Filter events by city
- Filter events by category
- Store events in PostgreSQL
- Avoid duplicate events using the source URL
- Trigger the scraper from the frontend
- Separate REST API for event access
- Separate REST API for scraper operations
- Containerized deployment using Docker and Docker Compose

## 3. Architecture

The application contains the following components:

- Frontend Service
- Event API Service
- Scraper Service
- PostgreSQL Database

Basic architecture:

```text
User
 |
Frontend Service
 |
Event API Service
 |
PostgreSQL Database

Frontend Service
 |
Scraper Service
 |
PostgreSQL Database
```

## 4. Microservices

### 4.1 Frontend Service

The frontend is a simple HTML, CSS and JavaScript web interface. It allows users to view events and apply filters by city and category.

Runs locally on:

```text
http://127.0.0.1:3000
```

### 4.2 Event API Service

The Event API is developed using FastAPI. It exposes REST endpoints for managing and filtering events.

Runs locally on:

```text
http://127.0.0.1:8000
```

Main endpoints:

```text
GET /events
POST /events
GET /events/{event_id}
DELETE /events/{event_id}
```

### 4.3 Scraper Service

The Scraper Service is developed using FastAPI. It simulates the collection of public events from external sources and stores them in the database.

Runs locally on:

```text
http://127.0.0.1:8001
```

Main endpoints:

```text
GET /scrape/status
GET /scrape/preview
POST /scrape
```

## 5. Database

The application uses PostgreSQL.

Main table:

```text
events
```

Fields:

```text
id
title
description
city
location
category
event_date
source_name
source_url
created_at
updated_at
```

The `source_url` field is unique and is used to avoid duplicate events.

## 6. Technologies Used

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- HTML
- CSS
- JavaScript
- Docker
- Docker Compose
- Nginx for serving the frontend

## 7. How to Run the Project Locally

From the root folder of the project, run:

```bash
docker compose up --build
```

After the containers start, open:

```text
Frontend:
http://127.0.0.1:3000

Event API Swagger:
http://127.0.0.1:8000/docs

Scraper Service Swagger:
http://127.0.0.1:8001/docs
```

## 8. Docker Services

The Docker Compose setup starts the following services:

```text
postgres
event-api
scraper-service
frontend
```

Service ports:

```text
Frontend: 3000
Event API: 8000
Scraper Service: 8001
PostgreSQL: 5432
```

## 9. Example Usage

### View all events

```text
GET http://127.0.0.1:8000/events
```

### Filter events by city

```text
GET http://127.0.0.1:8000/events?city=Timisoara
```

### Filter events by category

```text
GET http://127.0.0.1:8000/events?category=Technology
```

### Preview scraped events

```text
GET http://127.0.0.1:8001/scrape/preview
```

### Run scraper

```text
POST http://127.0.0.1:8001/scrape
```

## 10. Cloud Deployment Plan

For Google Cloud Platform, the application can be deployed using:

- Cloud Run for the frontend
- Cloud Run for the Event API Service
- Cloud Run for the Scraper Service
- Cloud SQL for PostgreSQL
- Cloud Scheduler for periodically triggering the scraper
- Cloud Logging for logs
- Cloud Monitoring for service monitoring
- IAM for access control

Proposed GCP architecture:

```text
User
 |
Cloud Run - Frontend
 |
Cloud Run - Event API
 |
Cloud SQL - PostgreSQL


Cloud Scheduler
 |
Cloud Run - Scraper Service
 |
Cloud SQL - PostgreSQL
```

## 11. Cloud-Native Considerations

The project follows several cloud-native principles:

- The application is split into multiple independent services.
- Each service is containerized.
- Services can be deployed independently.
- The database is separated from the application logic.
- Configuration is provided through environment variables.
- The architecture can be migrated to managed Google Cloud services.
- Logging and monitoring can be handled using Google Cloud operations tools.

## 12. SLA Considerations

From an SLA perspective, the application can be improved in production by using managed GCP services:

- Cloud Run provides managed execution for containerized services.
- Cloud SQL provides managed database availability and backups.
- Cloud Monitoring can detect downtime and performance issues.
- Cloud Logging helps identify application errors.
- Multiple Cloud Run instances can be used to improve availability.
- Cloud Scheduler can automate periodic scraping tasks.

The most important services for availability are the Event API and the database, because users depend on them to view and filter events.

## 13. Project Status

Current implementation status:

- Frontend implemented
- Event API implemented
- Scraper Service implemented
- PostgreSQL integration implemented
- Dockerfiles implemented
- Docker Compose implemented
- Local containerized execution tested successfully
- Filtering by city and category tested successfully
- Scraper trigger from frontend tested successfully