from datetime import datetime


def collect_events():
    """
    This function simulates the extraction of events from public web sources.
    Later, this can be extended with requests and BeautifulSoup for real websites.
    """

    events = [
        {
            "title": "Tech Conference Timisoara",
            "description": "A technology conference for students and professionals.",
            "city": "Timisoara",
            "location": "Convention Center Timisoara",
            "category": "Technology",
            "event_date": datetime(2026, 7, 10, 10, 0),
            "source_name": "Demo Scraper",
            "source_url": "https://example.com/events/tech-conference-timisoara"
        },
        {
            "title": "Food Festival Cluj",
            "description": "Outdoor food festival with local restaurants.",
            "city": "Cluj-Napoca",
            "location": "Central Park",
            "category": "Food",
            "event_date": datetime(2026, 7, 15, 18, 0),
            "source_name": "Demo Scraper",
            "source_url": "https://example.com/events/food-festival-cluj"
        },
        {
            "title": "Theatre Night Bucuresti",
            "description": "Evening theatre performance in Bucharest.",
            "city": "Bucuresti",
            "location": "National Theatre",
            "category": "Theatre",
            "event_date": datetime(2026, 7, 20, 20, 0),
            "source_name": "Demo Scraper",
            "source_url": "https://example.com/events/theatre-night-bucuresti"
        },
        {
            "title": "Startup Meetup Iasi",
            "description": "Networking event for startup founders and students.",
            "city": "Iasi",
            "location": "Innovation Hub Iasi",
            "category": "Business",
            "event_date": datetime(2026, 8, 5, 17, 30),
            "source_name": "Demo Scraper",
            "source_url": "https://example.com/events/startup-meetup-iasi"
        }
    ]

    return events