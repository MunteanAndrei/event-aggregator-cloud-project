# Event Aggregator - Final Report

## 1. Application Description

The selected project follows the Red Pill direction, where the source code is developed from scratch. The application is called Event Aggregator and it is a web application based on a microservices architecture.

The main purpose of the application is to collect public event information, store it in a database, and expose the data through REST APIs. Users can access a web interface where they can view events and filter them by city or category.

The application contains two separate API interfaces:

- Event API Service
- Scraper Service

The Event API Service is responsible for exposing event data to the frontend. The Scraper Service is responsible for collecting event data and saving it into the database.

The application was developed locally using Docker and Docker Compose, but the architecture is designed so that it can be deployed on Google Cloud Platform.

---

## 2. Functional Requirements

The application provides the following main features:

- Display public events in a web interface
- Filter events by city
- Filter events by category
- Store event data in PostgreSQL
- Avoid duplicate events using the event source URL
- Trigger the scraper from the frontend
- Preview events collected by the scraper
- Expose event data through a REST API
- Expose scraper operations through a separate REST API
- Run all services using Docker Compose

---

## 3. Data Model

The main entity used by the application is the Event entity.

The database table is called:

```text
events
```

The table contains the following fields:

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

### Field Description

| Field | Description |
|---|---|
| id | Unique identifier of the event |
| title | Name of the event |
| description | Short description of the event |
| city | City where the event takes place |
| location | More specific event location |
| category | Event category, such as Music, Technology, Food or Business |
| event_date | Date and time of the event |
| source_name | Name of the source from which the event was collected |
| source_url | URL of the event source |
| created_at | Timestamp when the event was inserted |
| updated_at | Timestamp when the event was last updated |

The `source_url` field is unique and is used to prevent duplicate events from being inserted into the database.

---

## 4. Implementation Technologies

The following technologies were used:

```text
Python
FastAPI
SQLAlchemy
PostgreSQL
HTML
CSS
JavaScript
Docker
Docker Compose
Nginx
```

FastAPI was used for the backend microservices because it provides a simple way to build REST APIs and automatically generates Swagger documentation.

PostgreSQL was used as the relational database.

Docker was used to containerize all services.

Docker Compose was used to start the entire local system with a single command.

---

## 5. Local Microservices Architecture

The application contains the following services:

```text
frontend
event-api
scraper-service
postgres
```

### 5.1 Frontend Service

The frontend service is responsible for the user interface.

It allows the user to:

- View events
- Filter events by city
- Filter events by category
- Trigger the scraper service

The frontend is implemented using HTML, CSS and JavaScript and is served using Nginx.

Local URL:

```text
http://127.0.0.1:3000
```

---

### 5.2 Event API Service

The Event API Service is implemented using FastAPI.

Its main responsibilities are:

- Return all events
- Return filtered events
- Create events
- Return one event by ID
- Delete events

Local URL:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Main endpoints:

```text
GET /events
POST /events
GET /events/{event_id}
DELETE /events/{event_id}
```

---

### 5.3 Scraper Service

The Scraper Service is also implemented using FastAPI.

Its main responsibilities are:

- Check scraper status
- Preview collected events
- Insert collected events into PostgreSQL
- Skip duplicate events

Local URL:

```text
http://127.0.0.1:8001
```

Swagger documentation:

```text
http://127.0.0.1:8001/docs
```

Main endpoints:

```text
GET /scrape/status
GET /scrape/preview
POST /scrape
```

---

### 5.4 PostgreSQL Database

The database stores all collected events.

Both backend services communicate with the database:

- Event API Service reads and manages event data
- Scraper Service inserts collected event data

The frontend does not access the database directly.

---

## 6. Local Architecture Diagram

The local architecture can be described as follows:

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

## 7. Google Cloud Architecture

For the production deployment, the application was deployed on Google Cloud Platform using Cloud Run and Cloud Firestore.

The selected Google Cloud services are:

```text
Cloud Run
Cloud Firestore
Cloud Build
Artifact Registry
Cloud Logging
Cloud Monitoring
IAM
```

The deployed architecture is:

```text
User / Browser
      |
      v
Cloud Run - Event Aggregator Application
      |
      |--- Frontend
      |--- Event API
      |--- Scraper API
      |
      v
Cloud Firestore - events collection


Cloud Build
      |
      v
Builds container image from source code


Artifact Registry
      |
      v
Stores container image used by Cloud Run


Cloud Logging / Cloud Monitoring / IAM
```

The live application URL is:

```text
https://event-aggregator-app-373732692778.europe-west1.run.app/
```

The Firestore database stores event documents inside the `events` collection.

This deployment was selected because it reduces costs compared to a Cloud SQL deployment while still using managed Google Cloud services.

---

## 8. Description of GCP Components

### 8.1 Cloud Run

Cloud Run is used to deploy the containerized Event Aggregator application.

In the cloud version, the application contains:

```text
Frontend
Event API
Scraper API
```

inside one Cloud Run service.

Cloud Run was selected because it supports containerized applications, automatic scaling, HTTPS endpoints and a low-cost deployment model.

The deployed Cloud Run service is:

```text
event-aggregator-app
```

Live URL:

```text
https://event-aggregator-app-373732692778.europe-west1.run.app/
```

---

### 8.2 Cloud Firestore

Cloud Firestore is used as the managed cloud database.

The application stores events in the following collection:

```text
events
```

Each event document contains:

```text
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

Firestore was selected instead of Cloud SQL in order to reduce infrastructure costs while still using a managed Google Cloud storage service.

---

### 8.3 Cloud Build

Cloud Build was used automatically during deployment from source code.

When running the deployment command, Google Cloud built the container image from the source code and Dockerfile.

---

### 8.4 Artifact Registry

Artifact Registry stores the container image created by Cloud Build.

Cloud Run uses this image to start the deployed service.

---

### 8.5 Cloud Logging

Cloud Logging collects logs from the deployed Cloud Run service.

It can be used to inspect:

```text
API errors
scraper execution logs
Firestore connection errors
service startup logs
```

---

### 8.6 Cloud Monitoring

Cloud Monitoring can be used to observe the deployed Cloud Run service.

It can monitor:

```text
request count
error rate
latency
container health
availability
```

---

### 8.7 IAM

IAM controls access to Google Cloud resources.

It is used to allow the deployed Cloud Run service to access Firestore and to manage public access to the application.

---

## 9. Deployment Considerations

The local deployment is done using Docker Compose.

Command used to start the application:

```bash
docker compose up --build
```

This starts:

```text
frontend_service
event_api_service
scraper_service
event_aggregator_db
```

For GCP production deployment, the following steps can be used:

1. Build Docker images for each service
2. Push the images to Artifact Registry
3. Deploy each image to Cloud Run
4. Create a Cloud SQL PostgreSQL instance
5. Configure the database connection using environment variables
6. Configure Cloud Scheduler to call the scraper periodically
7. Enable Cloud Logging and Cloud Monitoring

---

## 10. Cloud-Native Maturity Evaluation

The application can be evaluated from a cloud-native maturity perspective using three main axes:

### 10.1 Service Decomposition

The application is split into multiple services:

```text
Frontend Service
Event API Service
Scraper Service
Database
```

Each service has a separate responsibility.

This improves modularity and makes the application easier to maintain.

---

### 10.2 Scalability and Elasticity

The proposed GCP deployment uses Cloud Run, which allows services to scale independently.

For example:

- The Event API can scale based on user traffic
- The Scraper Service can run only when needed
- The Frontend Service can scale separately

This is better than deploying the entire application as a single monolithic service.

---

### 10.3 Automation and Manageability

The application is containerized and can be deployed using automated tools.

Possible automation tools:

```text
Cloud Build
Artifact Registry
Cloud Run deployments
Cloud Scheduler
```

The use of environment variables makes the application easier to move between local and cloud environments.

---

## 11. SLA Considerations

From an SLA perspective, the most important components are:

```text
Frontend Service
Event API Service
Cloud SQL Database
```

If the Event API or the database is unavailable, users cannot view events.

The Scraper Service is less critical because the application can still display already collected events even if the scraper is temporarily unavailable.

### 11.1 Event API SLA Considerations

The Event API should be highly available because it is used directly by the frontend.

Possible improvements:

- Deploy the Event API on Cloud Run
- Allow multiple instances
- Monitor error rate and latency
- Use alerts for repeated failures

---

### 11.2 Database SLA Considerations

The database is critical because both backend services depend on it.

Possible improvements:

- Use Cloud SQL automated backups
- Enable high availability if required
- Monitor storage and connections
- Restrict access using IAM and network rules

---

### 11.3 Scraper SLA Considerations

The Scraper Service is not as critical as the Event API.

If it fails, existing events remain available.

Possible improvements:

- Use Cloud Scheduler retries
- Log scraper errors
- Monitor scraper execution results
- Send alerts if the scraper repeatedly fails

---

## 12. Testing

The following tests were performed locally:

- Event API started successfully
- Scraper Service started successfully
- PostgreSQL container started successfully
- Frontend started successfully
- Events were inserted into the database
- Duplicate events were skipped
- Events were displayed in the frontend
- Filtering by city worked successfully
- Filtering by category worked successfully
- Run Scraper button successfully called the Scraper Service
- All services were started using Docker Compose

---

## 13. Conclusion

The Event Aggregator project satisfies the requirements of the Red Pill direction.

The application was developed from scratch and follows a microservices architecture. It contains two separate API interfaces, one for event access and one for scraper operations.

The application uses PostgreSQL for data storage and is containerized using Docker. It can be deployed to Google Cloud Platform using Cloud Run, Cloud SQL and Cloud Scheduler.

The project demonstrates the use of cloud-native principles such as service separation, containerization, independent scalability and managed cloud services.