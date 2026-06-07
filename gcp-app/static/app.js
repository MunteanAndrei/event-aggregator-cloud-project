const API_URL = "/events";
const SCRAPER_URL = "/scrape";

async function loadEvents() {
    const city = document.getElementById("cityInput").value;
    const category = document.getElementById("categoryInput").value;

    let url = API_URL;
    const params = new URLSearchParams();

    if (city) {
        params.append("city", city);
    }

    if (category) {
        params.append("category", category);
    }

    if (params.toString()) {
        url += "?" + params.toString();
    }

    const response = await fetch(url);
    const events = await response.json();

    displayEvents(events);
}

function displayEvents(events) {
    const container = document.getElementById("eventsContainer");
    container.innerHTML = "";

    if (events.length === 0) {
        container.innerHTML = `<p class="empty">No events found. Click Run Scraper to collect events.</p>`;
        return;
    }

    events.forEach(event => {
        const eventDate = event.event_date
            ? new Date(event.event_date).toLocaleString()
            : "Date not available";

        const card = document.createElement("div");
        card.className = "event-card";

        card.innerHTML = `
            <span class="badge">${event.category || "General"}</span>
            <h2>${event.title}</h2>
            <p>${event.description || ""}</p>
            <p><strong>City:</strong> ${event.city}</p>
            <p><strong>Location:</strong> ${event.location || "Not specified"}</p>
            <p><strong>Date:</strong> ${eventDate}</p>
            <p><strong>Source:</strong> ${event.source_name}</p>
            <a href="${event.source_url}" target="_blank">View source</a>
        `;

        container.appendChild(card);
    });
}

async function runScraper() {
    const message = document.getElementById("scraperMessage");
    message.textContent = "Scraper is running...";

    try {
        const response = await fetch(SCRAPER_URL, {
            method: "POST"
        });

        const result = await response.json();

        message.textContent = `Scraper completed. Inserted: ${result.inserted_events}, duplicates skipped: ${result.skipped_duplicates}`;

        loadEvents();
    } catch (error) {
        message.textContent = "Error running scraper service.";
        console.error(error);
    }
}

function clearFilters() {
    document.getElementById("cityInput").value = "";
    document.getElementById("categoryInput").value = "";
    loadEvents();
}

loadEvents();