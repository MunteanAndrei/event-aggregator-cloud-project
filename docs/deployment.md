# Deployment Documentation

## 1. Overview

This document describes how the Event Aggregator application can be run locally using Docker Compose and how it can be deployed to Google Cloud Platform.

The application is composed of the following services:

```text
frontend
event-api
scraper-service
postgres
```

Each application service is containerized using Docker.

---

## 2. Local Deployment with Docker Compose

The local deployment uses Docker Compose to start all services together.

The services are defined in:

```text
docker-compose.yml
```

To start the project, run the following command from the root folder:

```bash
docker compose up --build
```

This command builds the Docker images and starts the containers.

---

## 3. Local URLs

After the containers are running, the services are available at:

```text
Frontend:
http://127.0.0.1:3000

Event API:
http://127.0.0.1:8000

Event API Swagger:
http://127.0.0.1:8000/docs

Scraper Service:
http://127.0.0.1:8001

Scraper Service Swagger:
http://127.0.0.1:8001/docs

PostgreSQL:
localhost:5432
```

---

## 4. Docker Containers

The project starts the following containers:

```text
frontend_service
event_api_service
scraper_service
event_aggregator_db
```

The frontend container uses Nginx to serve the static HTML, CSS and JavaScript files.

The backend services use Python and FastAPI.

The database container uses PostgreSQL.

---

## 5. Environment Variables

The backend services use the following environment variable:

```text
DATABASE_URL
```

In local Docker Compose, the value is:

```text
postgresql://events_user:events_password@postgres:5432/events_db
```

The hostname is `postgres` because the services communicate inside the Docker Compose network.

For local development outside Docker, the value is:

```text
postgresql://events_user:events_password@localhost:5432/events_db
```

---

## 6. Proposed Google Cloud Deployment

The application can be deployed to Google Cloud Platform using the following services:

```text
Cloud Run
Cloud SQL
Cloud Scheduler
Cloud Logging
Cloud Monitoring
IAM
Artifact Registry
Cloud Build
```

---

## 7. Cloud Run

Cloud Run can host the containerized services:

```text
frontend
event-api
scraper-service
```

Each service can be deployed independently.

Benefits:

- Managed container execution
- Automatic scaling
- HTTPS endpoints
- No manual server maintenance
- Independent deployment for each microservice

---

## 8. Cloud SQL

Cloud SQL can be used as a managed PostgreSQL database.

The local PostgreSQL container would be replaced by:

```text
Cloud SQL - PostgreSQL
```

Benefits:

- Managed database service
- Automatic backups
- High availability options
- Easier maintenance
- Integration with Cloud Run

---

## 9. Cloud Scheduler

Cloud Scheduler can be used to automatically call the scraper service.

Example usage:

```text
Call POST /scrape every 24 hours
```

This allows the application to collect new events periodically without manual interaction.

---

## 10. Artifact Registry

Artifact Registry can be used to store Docker images.

Possible images:

```text
event-api-image
scraper-service-image
frontend-image
```

The images can then be deployed to Cloud Run.

---

## 11. Cloud Build

Cloud Build can automate the build and deployment process.

A possible deployment flow:

```text
Push source code to repository
 |
Cloud Build builds Docker images
 |
Images are pushed to Artifact Registry
 |
Cloud Run services are updated
```

This improves the deployment process and reduces manual work.

---

## 12. Logging and Monitoring

Cloud Logging can collect logs from all Cloud Run services.

Cloud Monitoring can track:

```text
request count
latency
error rate
container health
database metrics
```

These services help identify availability and performance problems.

---

## 13. IAM and Security

IAM can be used to control access between services.

Examples:

```text
Cloud Run Event API can access Cloud SQL
Cloud Run Scraper Service can access Cloud SQL
Cloud Scheduler can invoke the Scraper Service
```

In a production setup, public access should be restricted where possible.

---

## 14. Deployment Summary

The local version uses:

```text
Docker Compose
PostgreSQL container
FastAPI containers
Nginx frontend container
```

The cloud version can use:

```text
Cloud Run for services
Cloud SQL for database
Cloud Scheduler for automation
Cloud Logging and Monitoring for observability
IAM for security
Artifact Registry and Cloud Build for deployment automation
```

This deployment approach satisfies the project requirement of moving the application to production using Google Cloud Platform services.