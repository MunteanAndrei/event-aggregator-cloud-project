# Application Architecture

## 1. Overview

The Event Aggregator application is designed using a microservices architecture. The system is split into independent services, each having a clear responsibility.

The main goal of the application is to collect public event data, store it in a database, and expose it through REST APIs so users can view and filter events.

The project is developed locally using Docker and Docker Compose, but the same architecture can be deployed to Google Cloud Platform using managed cloud services.

---

## 2. Local Architecture

The local version of the application contains four main components:

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

---

## 3. Local Components

### 3.1 Frontend Service

The frontend service is responsible for the user interface.

Technology used:

```text
HTML, CSS, JavaScript, Nginx
```

Responsibilities:

- Display events in card format
- Allow filtering by city
- Allow filtering by category
- Trigger the scraper service using a button
- Communicate with the Event API and Scraper API

Local URL:

```text
http://127.0.0.1:3000
```

---

### 3.2 Event API Service

The Event API Service is responsible for exposing event data to the frontend.

Technology used:

```text
Python, FastAPI, SQLAlchemy
```

Responsibilities:

- Return all events
- Filter events by city
- Filter events by category
- Filter events by source name
- Add new events
- Delete events
- Read data from PostgreSQL

Local URL:

```text
http://127.0.0.1:8000
```

---

### 3.3 Scraper Service

The Scraper Service is responsible for collecting event data.

Technology used:

```text
Python, FastAPI
```

Responsibilities:

- Provide scraper status
- Preview collected events
- Insert collected events into the database
- Skip duplicate events based on the unique source URL

Local URL:

```text
http://127.0.0.1:8001
```

---

### 3.4 PostgreSQL Database

The database stores all collected events.

Technology used:

```text
PostgreSQL
```

Main table:

```text
events
```

The database is accessed by both backend microservices:

- Event API Service
- Scraper Service

The frontend does not access the database directly.

---

## 4. Docker Architecture

The application is containerized using Docker.

The following containers are started using Docker Compose:

```text
frontend_service
event_api_service
scraper_service
event_aggregator_db
```

Docker Compose is used to define:

- Service images
- Build contexts
- Ports
- Environment variables
- Service dependencies
- Database volume

The local ports are:

```text
Frontend: 3000
Event API: 8000
Scraper Service: 8001
PostgreSQL: 5432
```

---

## 5. Data Flow

### 5.1 Viewing Events

```text
User
 |
Frontend Service
 |
GET /events
 |
Event API Service
 |
PostgreSQL Database
```

Steps:

1. The user opens the frontend application.
2. The frontend sends a request to the Event API.
3. The Event API reads events from PostgreSQL.
4. The Event API returns JSON data.
5. The frontend displays the events as cards.

---

### 5.2 Filtering Events

```text
User
 |
Frontend filters
 |
GET /events?city=Timisoara
 |
Event API Service
 |
PostgreSQL Database
```

Steps:

1. The user enters a city or category.
2. The frontend sends the selected filters as query parameters.
3. The Event API applies SQL filters.
4. The filtered result is returned to the frontend.

---

### 5.3 Running the Scraper

```text
User
 |
Frontend button
 |
POST /scrape
 |
Scraper Service
 |
PostgreSQL Database
```

Steps:

1. The user clicks the Run Scraper button.
2. The frontend sends a POST request to the Scraper Service.
3. The Scraper Service collects event data.
4. The service checks for duplicate source URLs.
5. New events are inserted into PostgreSQL.
6. A result message is returned to the frontend.

---

## 6. Proposed Google Cloud Architecture

For production deployment, the application can be moved to Google Cloud Platform.

Proposed GCP architecture:

```text
                         Google Cloud Platform

        User
         |
         v
   Cloud Run - Frontend
         |
         v
   Cloud Run - Event API
         |
         v
   Cloud SQL - PostgreSQL


   Cloud Scheduler
         |
         v
   Cloud Run - Scraper Service
         |
         v
   Cloud SQL - PostgreSQL


   Cloud Logging / Cloud Monitoring / IAM
```

---

## 7. Google Cloud Services

### 7.1 Cloud Run

Cloud Run can be used to deploy the three containerized services:

- Frontend Service
- Event API Service
- Scraper Service

Cloud Run is suitable because the services are already containerized using Docker.

Benefits:

- Managed container execution
- Automatic scaling
- HTTPS endpoints
- No server management
- Independent deployment for each microservice

---

### 7.2 Cloud SQL

Cloud SQL can be used as the managed PostgreSQL database.

Benefits:

- Managed relational database
- Backups
- High availability options
- Security configuration
- Easier maintenance compared to a manually configured database on a virtual machine

---

### 7.3 Cloud Scheduler

Cloud Scheduler can be used to trigger the scraper periodically.

Example:

```text
Run scraper every 24 hours
```

It would call:

```text
POST /scrape
```

on the Scraper Service deployed in Cloud Run.

---

### 7.4 Cloud Logging

Cloud Logging can collect logs from all Cloud Run services.

It can be used to inspect:

- API errors
- Scraper execution logs
- Database connection errors
- Service startup logs

---

### 7.5 Cloud Monitoring

Cloud Monitoring can be used to observe service health and performance.

It can monitor:

- Request count
- Error rate
- Latency
- Container instance usage
- Availability

---

### 7.6 IAM

IAM is used to control access between Google Cloud services.

Examples:

- Allow Cloud Run services to access Cloud SQL
- Allow Cloud Scheduler to call the Scraper Service
- Restrict public access where needed

---

## 8. Cloud-Native Maturity

The application follows several cloud-native principles.

### 8.1 Service Decomposition

The system is split into multiple services:

- Frontend
- Event API
- Scraper Service
- Database

Each service has a clear responsibility.

### 8.2 Containerization

Each application service has its own Dockerfile and can be built as an independent container image.

### 8.3 Scalability

The services can be scaled independently in Cloud Run.

For example:

- Event API can scale based on user traffic.
- Scraper Service can run only when needed.
- Frontend can scale separately from backend services.

### 8.4 Configuration

Configuration is provided through environment variables, especially the database connection string.

This makes the application easier to move from local development to cloud deployment.

### 8.5 Managed Services

The proposed cloud deployment uses managed services such as:

- Cloud Run
- Cloud SQL
- Cloud Scheduler
- Cloud Logging
- Cloud Monitoring

This reduces operational work.

---

## 9. SLA Considerations

From an SLA perspective, the most critical components are:

- Event API Service
- PostgreSQL Database
- Frontend Service

If the Scraper Service is temporarily unavailable, users can still access already collected events. However, new events will not be collected until the scraper is available again.

### 9.1 Event API Availability

The Event API should have high availability because it is used by the frontend to display events.

Possible improvements:

- Deploy Event API on Cloud Run
- Allow multiple instances
- Monitor error rate and latency
- Use health checks

### 9.2 Database Availability

The database is critical because both backend services depend on it.

Possible improvements:

- Use Cloud SQL automated backups
- Enable high availability if needed
- Monitor CPU, memory, storage and connections
- Restrict access using IAM and networking rules

### 9.3 Scraper Availability

The scraper is less critical than the Event API. If it fails, the application can still show existing events.

Possible improvements:

- Use Cloud Scheduler retries
- Log scraper errors
- Store scraper execution logs
- Send alerts if repeated failures occur

---

## 10. Summary

The proposed architecture satisfies the project requirements because:

- The application is developed from scratch.
- It uses a microservices architecture.
- It contains at least two separate API interfaces.
- It uses PostgreSQL for data storage.
- It is containerized using Docker.
- It can be deployed to Google Cloud using Cloud Run and Cloud SQL.
- It includes cloud-native considerations and SLA-related design aspects.