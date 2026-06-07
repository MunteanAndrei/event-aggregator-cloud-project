# Event Aggregator - Proiect Cloud Computing

## 1. Prezentare generală

Event Aggregator este o aplicație web dezvoltată folosind o arhitectură bazată pe microservicii. Aplicația colectează informații despre evenimente publice, le stochează într-o bază de date și expune API-uri REST pentru listarea și filtrarea evenimentelor.

Proiectul urmează direcția **Red Pill**, ceea ce înseamnă că aplicația a fost dezvoltată de la zero.

Utilizatorii pot vizualiza evenimentele printr-o interfață web și le pot filtra după oraș sau categorie. Scraperul poate fi pornit manual din interfața web pentru a colecta evenimente.

Aplicația a fost rulată local folosind Docker Compose și PostgreSQL, iar varianta de producție a fost deployată pe Google Cloud Platform folosind **Cloud Run** și **Cloud Firestore**.

---

## 2. Funcționalități principale

- Afișarea evenimentelor într-o interfață web
- Filtrarea evenimentelor după oraș
- Filtrarea evenimentelor după categorie
- Stocarea evenimentelor într-o bază de date
- Evitarea duplicatelor folosind câmpul `source_url`
- Pornirea scraperului din frontend
- API REST separat pentru accesarea evenimentelor
- API REST separat pentru operațiile de scraping
- Rulare locală folosind Docker și Docker Compose
- Deployment pe Google Cloud Platform folosind Cloud Run și Firestore

---

## 3. Arhitectură

Aplicația conține următoarele componente în varianta locală:

- Frontend Service
- Event API Service
- Scraper Service
- PostgreSQL Database

Arhitectura locală de bază:

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

În varianta Google Cloud, aplicația este rulată într-un serviciu Cloud Run, iar datele sunt salvate în Cloud Firestore:

```text
User / Browser
 |
Cloud Run - Event Aggregator Application
 |
 |--- Frontend
 |--- Event API
 |--- Scraper API
 |
Cloud Firestore - events collection
```

---

## 4. Microservicii locale

### 4.1 Frontend Service

Frontend-ul este o interfață web simplă realizată folosind HTML, CSS și JavaScript. Acesta permite utilizatorilor să vizualizeze evenimentele și să aplice filtre după oraș și categorie.

Rulează local pe:

```text
http://127.0.0.1:3000
```

---

### 4.2 Event API Service

Event API este dezvoltat folosind FastAPI. Acesta expune endpoint-uri REST pentru gestionarea și filtrarea evenimentelor.

Rulează local pe:

```text
http://127.0.0.1:8000
```

Endpoint-uri principale:

```text
GET /events
POST /events
GET /events/{event_id}
DELETE /events/{event_id}
```

---

### 4.3 Scraper Service

Scraper Service este dezvoltat folosind FastAPI. Acesta simulează colectarea evenimentelor publice din surse externe și le salvează în baza de date.

Rulează local pe:

```text
http://127.0.0.1:8001
```

Endpoint-uri principale:

```text
GET /scrape/status
GET /scrape/preview
POST /scrape
```

---

## 5. Baza de date

În varianta locală, aplicația folosește PostgreSQL.

Tabel principal:

```text
events
```

În varianta cloud, aplicația folosește Cloud Firestore.

Colecție principală:

```text
events
```

Câmpurile unui eveniment sunt:

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

Câmpul `source_url` este folosit pentru a evita inserarea evenimentelor duplicate.

---

## 6. Tehnologii folosite

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Cloud Firestore
- HTML
- CSS
- JavaScript
- Docker
- Docker Compose
- Nginx
- Cloud Run
- Cloud Build
- Artifact Registry

---

## 7. Rulare locală

Din folderul principal al proiectului, se rulează:

```bash
docker compose up --build
```

După pornirea containerelor, aplicația poate fi accesată la:

```text
Frontend:
http://127.0.0.1:3000

Event API Swagger:
http://127.0.0.1:8000/docs

Scraper Service Swagger:
http://127.0.0.1:8001/docs
```

---

## 8. Servicii Docker

Docker Compose pornește următoarele servicii:

```text
postgres
event-api
scraper-service
frontend
```

Porturi folosite:

```text
Frontend: 3000
Event API: 8000
Scraper Service: 8001
PostgreSQL: 5432
```

---

## 9. Exemple de utilizare locală

### Vizualizarea tuturor evenimentelor

```text
GET http://127.0.0.1:8000/events
```

### Filtrare după oraș

```text
GET http://127.0.0.1:8000/events?city=Timisoara
```

### Filtrare după categorie

```text
GET http://127.0.0.1:8000/events?category=Technology
```

### Previzualizarea evenimentelor colectate de scraper

```text
GET http://127.0.0.1:8001/scrape/preview
```

### Pornirea scraperului

```text
POST http://127.0.0.1:8001/scrape
```

---

## 10. Deployment pe Google Cloud Platform

Varianta cloud a aplicației este deployată pe Google Cloud Platform folosind:

- Cloud Run pentru rularea aplicației containerizate
- Cloud Firestore pentru stocarea evenimentelor
- Cloud Build pentru construirea imaginii Docker
- Artifact Registry pentru stocarea imaginii container
- Cloud Logging pentru loguri
- Cloud Monitoring pentru monitorizare
- IAM pentru controlul accesului

Aplicația live:

```text
https://event-aggregator-app-373732692778.europe-west1.run.app/
```

Endpoint-uri live:

```text
Events API:
https://event-aggregator-app-373732692778.europe-west1.run.app/events

Scraper Preview:
https://event-aggregator-app-373732692778.europe-west1.run.app/scrape/preview

Swagger:
https://event-aggregator-app-373732692778.europe-west1.run.app/docs
```

---

## 11. Arhitectura GCP

Arhitectura folosită în Google Cloud Platform:

```text
User / Browser
 |
Cloud Run - Event Aggregator Application
 |
 |--- Frontend
 |--- Event API
 |--- Scraper API
 |
Cloud Firestore - events collection


Cloud Build
 |
Builds Docker image from source code


Artifact Registry
 |
Stores container image used by Cloud Run


Cloud Logging / Cloud Monitoring / IAM
```

Pentru reducerea costurilor, varianta cloud folosește Cloud Firestore în loc de Cloud SQL. Firestore este suficient pentru acest proiect, deoarece aplicația stochează documente simple de tip eveniment.

---

## 12. Considerente cloud-native

Proiectul respectă mai multe principii cloud-native:

- Aplicația este împărțită logic în componente separate
- Serviciile sunt containerizate
- Backend-ul expune API-uri REST clare
- Configurația este separată de cod
- Deployment-ul se face pe servicii gestionate din Google Cloud
- Aplicația poate fi monitorizată prin Cloud Logging și Cloud Monitoring
- Varianta locală poate fi rulată complet prin Docker Compose
- Varianta cloud poate fi extinsă ulterior în servicii Cloud Run separate

În varianta locală, aplicația este împărțită în microservicii separate. În varianta cloud, pentru reducerea costurilor, frontend-ul, Event API și Scraper API sunt grupate într-un singur serviciu Cloud Run, dar separarea logică a API-urilor este păstrată.

---

## 13. Considerente SLA

Din perspectiva SLA, cele mai importante componente sunt:

- Cloud Run Service
- Cloud Firestore
- Event API
- Frontend

Dacă Event API sau Firestore nu sunt disponibile, utilizatorii nu pot vizualiza evenimentele. Scraper API este mai puțin critic, deoarece aplicația poate afișa în continuare evenimentele deja salvate.

Îmbunătățiri posibile pentru producție:

- monitorizarea latenței și a ratei de erori în Cloud Monitoring
- analizarea logurilor în Cloud Logging
- configurarea de alerte pentru erori repetate
- creșterea numărului maxim de instanțe Cloud Run dacă traficul crește
- rularea periodică a scraperului prin Cloud Scheduler
- export periodic al datelor din Firestore pentru backup

---

## 14. Status proiect

Statusul curent al implementării:

- Frontend implementat
- Event API implementat
- Scraper API implementat
- PostgreSQL integrat pentru rulare locală
- Cloud Firestore integrat pentru rulare în GCP
- Dockerfile-uri implementate
- Docker Compose implementat
- Rulare locală containerizată testată cu succes
- Filtrare după oraș și categorie testată cu succes
- Butonul Run Scraper testat cu succes
- Deployment pe Cloud Run realizat cu succes
- Stocarea datelor în Firestore testată cu succes

---

## 15. Repository

Repository GitHub:

```text
https://github.com/MunteanAndrei/event-aggregator-cloud-project
```

Aplicație live:

```text
https://event-aggregator-app-373732692778.europe-west1.run.app/
```