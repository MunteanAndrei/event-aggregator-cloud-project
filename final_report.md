# Event Aggregator - Raport final

## 1. Descrierea aplicației

Proiectul ales urmează direcția Red Pill, ceea ce înseamnă că aplicația a fost dezvoltată de la zero. Aplicația se numește **Event Aggregator** și este o aplicație web bazată pe o arhitectură de tip microservicii.

Scopul principal al aplicației este colectarea informațiilor despre evenimente publice, stocarea acestora într-o bază de date și expunerea datelor prin interfețe API REST. Utilizatorii pot accesa o interfață web unde pot vizualiza evenimentele și le pot filtra după oraș sau categorie.

Aplicația conține două interfețe API principale:

- **Event API**, pentru accesarea și filtrarea evenimentelor;
- **Scraper API**, pentru colectarea și inserarea evenimentelor în baza de date.

În varianta locală, aplicația a fost dezvoltată folosind Docker, Docker Compose și PostgreSQL. Pentru varianta de producție pe Google Cloud Platform, aplicația a fost deployată folosind **Cloud Run** și **Cloud Firestore**, pentru a reduce costurile și pentru a folosi servicii gestionate de Google Cloud.

---

## 2. Funcționalități principale

Aplicația oferă următoarele funcționalități:

- afișarea evenimentelor într-o interfață web;
- filtrarea evenimentelor după oraș;
- filtrarea evenimentelor după categorie;
- stocarea evenimentelor într-o bază de date;
- evitarea duplicatelor folosind câmpul `source_url`;
- rularea scraperului din interfața web;
- previzualizarea evenimentelor colectate de scraper;
- expunerea datelor printr-un API REST pentru evenimente;
- expunerea operațiilor de scraping printr-un API REST separat;
- rularea locală a aplicației folosind Docker Compose;
- deployment pe Google Cloud Platform folosind Cloud Run și Firestore.

---

## 3. Modelul de date

Entitatea principală folosită de aplicație este entitatea **Event**.

În varianta locală, datele sunt stocate într-un tabel PostgreSQL numit:

```text
events
```

În varianta cloud, datele sunt stocate în Cloud Firestore într-o colecție numită:

```text
events
```

Câmpurile principale ale unui eveniment sunt:

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

### Descrierea câmpurilor

| Câmp | Descriere |
|---|---|
| id | Identificatorul unic al evenimentului |
| title | Titlul evenimentului |
| description | Descriere scurtă a evenimentului |
| city | Orașul în care are loc evenimentul |
| location | Locația exactă sau aproximativă |
| category | Categoria evenimentului, de exemplu Music, Technology, Food, Business |
| event_date | Data și ora evenimentului |
| source_name | Numele sursei din care a fost colectat evenimentul |
| source_url | URL-ul sursei evenimentului |
| created_at | Data la care evenimentul a fost inserat |
| updated_at | Data ultimei actualizări |

Câmpul `source_url` este folosit pentru a preveni inserarea evenimentelor duplicate. Dacă un eveniment cu același `source_url` există deja, acesta este ignorat de scraper.

---

## 4. Tehnologii folosite

Pentru implementarea proiectului au fost folosite următoarele tehnologii:

```text
Python
FastAPI
SQLAlchemy
PostgreSQL
Cloud Firestore
HTML
CSS
JavaScript
Docker
Docker Compose
Nginx
Cloud Run
Cloud Build
Artifact Registry
```

FastAPI a fost folosit pentru implementarea API-urilor, deoarece permite dezvoltarea rapidă a serviciilor REST și generează automat documentație Swagger.

PostgreSQL a fost folosit local pentru testarea aplicației într-un mediu apropiat de unul real.

Cloud Firestore a fost folosit în varianta cloud deoarece este un serviciu gestionat, are costuri reduse pentru un proiect mic și este acceptat în cerințele proiectului ca soluție de stocare în Google Cloud.

Docker a fost folosit pentru containerizarea aplicației, iar Docker Compose pentru rularea locală a tuturor serviciilor.

---

## 5. Arhitectura locală bazată pe microservicii

În varianta locală, aplicația conține următoarele servicii:

```text
frontend
event-api
scraper-service
postgres
```

### 5.1 Frontend Service

Frontend-ul este responsabil pentru interfața cu utilizatorul.

Acesta permite:

- vizualizarea evenimentelor;
- filtrarea după oraș;
- filtrarea după categorie;
- rularea scraperului printr-un buton.

Frontend-ul este implementat folosind HTML, CSS și JavaScript și este servit local prin Nginx.

URL local:

```text
http://127.0.0.1:3000
```

---

### 5.2 Event API Service

Event API Service este implementat folosind FastAPI.

Responsabilități principale:

- returnarea tuturor evenimentelor;
- filtrarea evenimentelor;
- crearea unui eveniment;
- returnarea unui eveniment după ID;
- ștergerea unui eveniment.

URL local:

```text
http://127.0.0.1:8000
```

Documentație Swagger locală:

```text
http://127.0.0.1:8000/docs
```

Endpoint-uri principale:

```text
GET /events
POST /events
GET /events/{event_id}
DELETE /events/{event_id}
```

---

### 5.3 Scraper Service

Scraper Service este implementat tot cu FastAPI.

Responsabilități principale:

- verificarea statusului scraperului;
- previzualizarea evenimentelor colectate;
- inserarea evenimentelor în baza de date;
- evitarea evenimentelor duplicate.

URL local:

```text
http://127.0.0.1:8001
```

Documentație Swagger locală:

```text
http://127.0.0.1:8001/docs
```

Endpoint-uri principale:

```text
GET /scrape/status
GET /scrape/preview
POST /scrape
```

---

### 5.4 PostgreSQL Database

În varianta locală, PostgreSQL este folosit pentru stocarea evenimentelor.

Ambele servicii backend comunică cu baza de date:

- Event API Service citește și gestionează evenimentele;
- Scraper Service inserează evenimentele colectate.

Frontend-ul nu comunică direct cu baza de date, ci doar prin API-uri.

---

## 6. Arhitectura locală

Arhitectura locală poate fi reprezentată astfel:

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

Această arhitectură demonstrează separarea responsabilităților între componente și respectă principiile unei aplicații bazate pe microservicii.

---

## 7. Arhitectura Google Cloud Platform

Pentru deployment-ul în producție, aplicația a fost publicată pe Google Cloud Platform folosind **Cloud Run** și **Cloud Firestore**.

Serviciile Google Cloud folosite sunt:

```text
Cloud Run
Cloud Firestore
Cloud Build
Artifact Registry
Cloud Logging
Cloud Monitoring
IAM
```

Aplicația live este disponibilă la:

```text
https://event-aggregator-app-373732692778.europe-west1.run.app/
```

Arhitectura cloud folosită este:

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

În varianta cloud, aplicația este rulată într-un singur serviciu Cloud Run. Acesta conține interfața web, Event API și Scraper API. Datele sunt salvate în Cloud Firestore, în colecția `events`.

Această variantă a fost aleasă pentru a reduce costurile față de o soluție bazată pe Cloud SQL, păstrând totuși utilizarea unor servicii gestionate din Google Cloud Platform.

---

## 8. Descrierea componentelor GCP

### 8.1 Cloud Run

Cloud Run este folosit pentru rularea aplicației containerizate.

În varianta cloud, aplicația conține într-un singur serviciu:

```text
Frontend
Event API
Scraper API
```

Cloud Run a fost ales deoarece permite rularea containerelor fără administrarea directă a serverelor. De asemenea, oferă scalare automată, endpoint HTTPS și un model de cost potrivit pentru proiecte mici.

Serviciul deployat se numește:

```text
event-aggregator-app
```

URL live:

```text
https://event-aggregator-app-373732692778.europe-west1.run.app/
```

---

### 8.2 Cloud Firestore

Cloud Firestore este folosit ca bază de date gestionată în cloud.

Aplicația stochează evenimentele în colecția:

```text
events
```

Fiecare document din colecție conține câmpurile:

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

Firestore a fost ales în locul Cloud SQL pentru a reduce costurile și pentru a folosi un serviciu gestionat de Google Cloud. Pentru un proiect de dimensiuni mici, Firestore este suficient pentru stocarea și citirea evenimentelor.

---

### 8.3 Cloud Build

Cloud Build a fost folosit automat în timpul deployment-ului.

La rularea comenzii de deployment, Google Cloud a construit imaginea Docker pornind de la codul sursă și de la fișierul Dockerfile.

---

### 8.4 Artifact Registry

Artifact Registry este folosit pentru stocarea imaginii container create de Cloud Build.

Cloud Run folosește această imagine pentru a porni serviciul deployat.

---

### 8.5 Cloud Logging

Cloud Logging colectează logurile generate de serviciul Cloud Run.

Acesta poate fi folosit pentru:

```text
erori API
loguri de execuție ale scraperului
erori de conectare la Firestore
loguri de pornire ale serviciului
```

---

### 8.6 Cloud Monitoring

Cloud Monitoring poate fi folosit pentru observarea aplicației deployate.

Poate monitoriza:

```text
numărul de request-uri
rata de erori
latența
starea containerului
disponibilitatea serviciului
```

---

### 8.7 IAM

IAM controlează accesul la resursele Google Cloud.

În acest proiect, IAM este relevant pentru:

- permisiunea serviciului Cloud Run de a accesa Firestore;
- gestionarea accesului public la aplicație;
- securizarea resurselor cloud.

---

## 9. Deployment

### 9.1 Deployment local

Local, aplicația este rulată folosind Docker Compose.

Comanda folosită:

```bash
docker compose up --build
```

Aceasta pornește următoarele containere:

```text
frontend_service
event_api_service
scraper_service
event_aggregator_db
```

URL-uri locale:

```text
Frontend:
http://127.0.0.1:3000

Event API:
http://127.0.0.1:8000

Scraper Service:
http://127.0.0.1:8001
```

---

### 9.2 Deployment pe Google Cloud Platform

Pentru varianta cloud, a fost creat folderul `gcp-app`, care conține o versiune adaptată pentru Cloud Run și Firestore.

Deployment-ul a fost realizat cu comanda:

```bash
gcloud run deploy event-aggregator-app \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --max-instances 1
```

Această comandă a realizat următorii pași:

1. a încărcat codul sursă în Google Cloud;
2. a construit imaginea Docker folosind Cloud Build;
3. a salvat imaginea în Artifact Registry;
4. a creat serviciul Cloud Run;
5. a expus aplicația public printr-un URL HTTPS.

URL-ul aplicației live este:

```text
https://event-aggregator-app-373732692778.europe-west1.run.app/
```

---

## 10. Evaluarea maturității cloud-native

Aplicația poate fi evaluată din perspectiva arhitecturii cloud-native pe trei axe principale: descompunerea în servicii, scalabilitatea și automatizarea.

### 10.1 Descompunerea în servicii

În varianta locală, aplicația este împărțită în servicii separate:

```text
Frontend Service
Event API Service
Scraper Service
Database
```

Fiecare serviciu are o responsabilitate clară.

Această separare ajută la mentenanță, testare și extindere.

În varianta cloud, pentru reducerea costurilor, serviciile sunt grupate într-un singur serviciu Cloud Run, dar interfețele API rămân separate logic:

```text
Event API
Scraper API
```

---

### 10.2 Scalabilitate și elasticitate

Cloud Run permite scalarea automată a aplicației în funcție de trafic.

Pentru reducerea costurilor, deployment-ul a fost configurat cu:

```text
--max-instances 1
```

Astfel, aplicația poate rula cu costuri minime, dar poate fi extinsă ulterior prin creșterea numărului de instanțe.

Într-o variantă de producție mai avansată, Event API și Scraper API ar putea fi deployate ca servicii Cloud Run separate, pentru scalare independentă.

---

### 10.3 Automatizare și administrare

Deployment-ul folosește servicii gestionate:

```text
Cloud Build
Artifact Registry
Cloud Run
Cloud Firestore
```

Cloud Build automatizează construirea imaginii Docker, iar Artifact Registry stochează imaginea. Cloud Run rulează aplicația fără a necesita administrarea unui server.

Prin folosirea variabilelor de mediu și a serviciilor gestionate, aplicația poate fi mutată mai ușor între mediul local și mediul cloud.

---

## 11. Considerente SLA

Din perspectiva SLA, cele mai importante componente sunt:

```text
Cloud Run Service
Cloud Firestore
Frontend
Event API
```

Dacă Event API sau Firestore nu sunt disponibile, utilizatorii nu pot vizualiza evenimentele.

Scraper API este mai puțin critic, deoarece aplicația poate afișa în continuare evenimentele deja colectate, chiar dacă scraperul nu rulează temporar.

### 11.1 Disponibilitatea Event API

Event API trebuie să fie disponibil deoarece frontend-ul depinde de el pentru afișarea evenimentelor.

Îmbunătățiri posibile:

- monitorizarea ratei de erori;
- monitorizarea latenței;
- configurarea de alerte;
- creșterea numărului maxim de instanțe Cloud Run dacă traficul crește.

---

### 11.2 Disponibilitatea bazei de date Firestore

Firestore este componenta critică pentru stocarea evenimentelor.

Îmbunătățiri posibile:

- monitorizarea operațiilor de citire și scriere;
- verificarea erorilor în Cloud Logging;
- folosirea regulilor IAM pentru controlul accesului;
- export periodic al datelor pentru backup, dacă proiectul devine mai mare.

---

### 11.3 Disponibilitatea Scraper API

Scraper API este important pentru actualizarea datelor, dar nu este la fel de critic ca Event API.

Dacă scraperul eșuează, evenimentele deja salvate rămân disponibile.

Îmbunătățiri posibile:

- logarea execuțiilor scraperului;
- monitorizarea răspunsului endpoint-ului `/scrape`;
- configurarea unei rulări periodice cu Cloud Scheduler;
- alerte în cazul unor erori repetate.

---

## 12. Testare

Au fost realizate următoarele teste:

### Teste locale

- Event API pornește corect;
- Scraper Service pornește corect;
- containerul PostgreSQL pornește corect;
- frontend-ul pornește corect;
- evenimentele sunt inserate în baza de date;
- evenimentele duplicate sunt ignorate;
- evenimentele sunt afișate în frontend;
- filtrarea după oraș funcționează;
- filtrarea după categorie funcționează;
- butonul Run Scraper apelează Scraper Service;
- toate serviciile pornesc folosind Docker Compose.

### Teste pe Google Cloud

- aplicația Cloud Run este accesibilă public;
- interfața web se încarcă din Cloud Run;
- endpoint-ul `/events` returnează evenimentele din Firestore;
- endpoint-ul `/scrape/preview` returnează evenimentele colectate;
- endpoint-ul `/scrape` inserează evenimente în Firestore;
- colecția `events` este vizibilă în Cloud Firestore;
- filtrarea după oraș și categorie funcționează în aplicația live.

---

## 13. Linkuri utile

Repository GitHub:

```text
https://github.com/MunteanAndrei/event-aggregator-cloud-project
```

Aplicație live GCP:

```text
https://event-aggregator-app-373732692778.europe-west1.run.app/
```

Events API live:

```text
https://event-aggregator-app-373732692778.europe-west1.run.app/events
```

Scraper Preview live:

```text
https://event-aggregator-app-373732692778.europe-west1.run.app/scrape/preview
```

Swagger live:

```text
https://event-aggregator-app-373732692778.europe-west1.run.app/docs
```

---

## 14. Concluzie

Proiectul **Event Aggregator** îndeplinește cerințele direcției Red Pill, deoarece aplicația a fost dezvoltată de la zero.

Aplicația folosește o arhitectură bazată pe microservicii în varianta locală și conține două interfețe API separate: Event API și Scraper API.

Pentru stocarea datelor, aplicația folosește PostgreSQL în mediul local și Cloud Firestore în mediul Google Cloud. Deployment-ul în cloud a fost realizat folosind Cloud Run, Cloud Build și Artifact Registry.

Proiectul demonstrează folosirea unor principii cloud-native precum separarea responsabilităților, containerizarea, deployment-ul pe servicii gestionate, scalarea automată și monitorizarea prin servicii Google Cloud.