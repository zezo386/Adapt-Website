from fastapi import FastAPI,Query
from typing import Optional
from pydantic import BaseModel
import sqlite3
import json

conn = sqlite3.connect('events.db')
cursor = conn.cursor()


app = FastAPI()


events_db = [
    # USA Events
    {"id": 1, "country": "USA", "city": "New York", "date": "2025-04-15", "tags": ["technology", "programming", "ai", "cloud"]},
    {"id": 2, "country": "USA", "city": "San Francisco", "date": "2025-05-20", "tags": ["data-science", "machine-learning", "analytics", "python"]},
    {"id": 3, "country": "USA", "city": "New York", "date": "2025-06-10", "tags": ["design", "ux", "ui", "workshop"]},
    {"id": 4, "country": "USA", "city": "Boston", "date": "2025-07-08", "tags": ["healthcare", "medical", "research", "biotech"]},
    {"id": 5, "country": "USA", "city": "Seattle", "date": "2025-08-12", "tags": ["cloud", "aws", "devops", "infrastructure"]},
    {"id": 6, "country": "USA", "city": "Austin", "date": "2025-03-14", "tags": ["music", "festival", "live", "entertainment"]},
    {"id": 7, "country": "USA", "city": "Chicago", "date": "2025-09-22", "tags": ["marketing", "advertising", "digital", "social-media"]},
    {"id": 8, "country": "USA", "city": "Los Angeles", "date": "2025-10-05", "tags": ["film", "entertainment", "media", "production"]},
    {"id": 9, "country": "USA", "city": "San Diego", "date": "2025-11-18", "tags": ["biotech", "research", "science", "healthcare"]},
    {"id": 10, "country": "USA", "city": "Denver", "date": "2025-06-25", "tags": ["outdoor", "sports", "adventure", "wellness"]},
    {"id": 11, "country": "USA", "city": "Miami", "date": "2025-02-28", "tags": ["finance", "investing", "crypto", "blockchain"]},
    {"id": 12, "country": "USA", "city": "Atlanta", "date": "2025-09-05", "tags": ["music", "hip-hop", "culture", "entertainment"]},
    {"id": 13, "country": "USA", "city": "Portland", "date": "2025-04-22", "tags": ["sustainability", "green", "environment", "eco"]},
    {"id": 14, "country": "USA", "city": "Washington DC", "date": "2025-03-03", "tags": ["politics", "government", "policy", "diplomacy"]},
    {"id": 15, "country": "USA", "city": "Philadelphia", "date": "2025-10-15", "tags": ["education", "academic", "research", "university"]},
    {"id": 16, "country": "USA", "city": "Houston", "date": "2025-07-20", "tags": ["space", "aerospace", "nasa", "engineering"]},
    {"id": 17, "country": "USA", "city": "Phoenix", "date": "2025-11-05", "tags": ["real-estate", "construction", "development", "property"]},
    {"id": 18, "country": "USA", "city": "Dallas", "date": "2025-08-25", "tags": ["business", "entrepreneurship", "startup", "networking"]},
    {"id": 19, "country": "USA", "city": "San Jose", "date": "2025-05-12", "tags": ["hardware", "semiconductors", "tech", "engineering"]},
    {"id": 20, "country": "USA", "city": "Pittsburgh", "date": "2025-06-18", "tags": ["robotics", "ai", "automation", "manufacturing"]},
    
    # UK Events
    {"id": 21, "country": "UK", "city": "London", "date": "2025-04-02", "tags": ["finance", "banking", "fintech", "investment"]},
    {"id": 22, "country": "UK", "city": "Manchester", "date": "2025-05-30", "tags": ["sports", "football", "athletics", "fitness"]},
    {"id": 23, "country": "UK", "city": "London", "date": "2025-09-15", "tags": ["fashion", "design", "luxury", "retail"]},
    {"id": 24, "country": "UK", "city": "Birmingham", "date": "2025-10-20", "tags": ["manufacturing", "industry", "engineering", "automotive"]},
    {"id": 25, "country": "UK", "city": "Edinburgh", "date": "2025-08-08", "tags": ["arts", "festival", "culture", "performance"]},
    {"id": 26, "country": "UK", "city": "Glasgow", "date": "2025-07-12", "tags": ["music", "indie", "live", "festival"]},
    {"id": 27, "country": "UK", "city": "Liverpool", "date": "2025-03-18", "tags": ["maritime", "shipping", "logistics", "trade"]},
    {"id": 28, "country": "UK", "city": "Bristol", "date": "2025-06-05", "tags": ["tech", "startup", "innovation", "digital"]},
    {"id": 29, "country": "UK", "city": "Oxford", "date": "2025-04-28", "tags": ["academic", "research", "science", "education"]},
    {"id": 30, "country": "UK", "city": "Cambridge", "date": "2025-09-28", "tags": ["biotech", "research", "science", "innovation"]},
    {"id": 31, "country": "UK", "city": "Leeds", "date": "2025-11-12", "tags": ["retail", "commerce", "business", "marketing"]},
    {"id": 32, "country": "UK", "city": "Sheffield", "date": "2025-05-05", "tags": ["steel", "industry", "manufacturing", "engineering"]},
    {"id": 33, "country": "UK", "city": "Newcastle", "date": "2025-10-10", "tags": ["nightlife", "entertainment", "music", "culture"]},
    {"id": 34, "country": "UK", "city": "Belfast", "date": "2025-06-22", "tags": ["tourism", "hospitality", "travel", "culture"]},
    {"id": 35, "country": "UK", "city": "Cardiff", "date": "2025-07-25", "tags": ["media", "broadcasting", "tv", "film"]},
    
    # Canada Events
    {"id": 36, "country": "Canada", "city": "Toronto", "date": "2025-09-10", "tags": ["film", "festival", "entertainment", "media"]},
    {"id": 37, "country": "Canada", "city": "Vancouver", "date": "2025-04-08", "tags": ["film", "production", "hollywood", "entertainment"]},
    {"id": 38, "country": "Canada", "city": "Montreal", "date": "2025-07-18", "tags": ["comedy", "festival", "performance", "arts"]},
    {"id": 39, "country": "Canada", "city": "Ottawa", "date": "2025-05-15", "tags": ["government", "policy", "politics", "public-service"]},
    {"id": 40, "country": "Canada", "city": "Calgary", "date": "2025-06-12", "tags": ["oil", "energy", "gas", "industry"]},
    {"id": 41, "country": "Canada", "city": "Edmonton", "date": "2025-08-20", "tags": ["festival", "arts", "culture", "performance"]},
    {"id": 42, "country": "Canada", "city": "Quebec City", "date": "2025-07-05", "tags": ["history", "heritage", "culture", "tourism"]},
    {"id": 43, "country": "Canada", "city": "Winnipeg", "date": "2025-09-25", "tags": ["arts", "culture", "indigenous", "heritage"]},
    {"id": 44, "country": "Canada", "city": "Halifax", "date": "2025-08-15", "tags": ["maritime", "ocean", "research", "fisheries"]},
    {"id": 45, "country": "Canada", "city": "Victoria", "date": "2025-05-25", "tags": ["tourism", "gardens", "nature", "heritage"]},
    
    # Germany Events
    {"id": 46, "country": "Germany", "city": "Berlin", "date": "2025-06-28", "tags": ["art", "culture", "nightlife", "music"]},
    {"id": 47, "country": "Germany", "city": "Munich", "date": "2025-09-20", "tags": ["beer", "oktoberfest", "festival", "bavarian"]},
    {"id": 48, "country": "Germany", "city": "Hamburg", "date": "2025-05-08", "tags": ["port", "maritime", "logistics", "trade"]},
    {"id": 49, "country": "Germany", "city": "Frankfurt", "date": "2025-04-12", "tags": ["finance", "banking", "trade", "business"]},
    {"id": 50, "country": "Germany", "city": "Cologne", "date": "2025-02-10", "tags": ["carnival", "festival", "culture", "music"]},
    {"id": 51, "country": "Germany", "city": "Stuttgart", "date": "2025-07-30", "tags": ["automotive", "cars", "engineering", "manufacturing"]},
    {"id": 52, "country": "Germany", "city": "Dusseldorf", "date": "2025-08-05", "tags": ["fashion", "retail", "design", "luxury"]},
    {"id": 53, "country": "Germany", "city": "Dresden", "date": "2025-09-08", "tags": ["baroque", "art", "history", "architecture"]},
    {"id": 54, "country": "Germany", "city": "Leipzig", "date": "2025-03-20", "tags": ["book-fair", "publishing", "literature", "culture"]},
    {"id": 55, "country": "Germany", "city": "Bremen", "date": "2025-10-25", "tags": ["space", "aerospace", "science", "research"]},
    
    # France Events
    {"id": 56, "country": "France", "city": "Paris", "date": "2025-03-05", "tags": ["fashion", "luxury", "design", "haute-couture"]},
    {"id": 57, "country": "France", "city": "Lyon", "date": "2025-04-18", "tags": ["gastronomy", "food", "wine", "culinary"]},
    {"id": 58, "country": "France", "city": "Marseille", "date": "2025-06-15", "tags": ["maritime", "mediterranean", "culture", "port"]},
    {"id": 59, "country": "France", "city": "Toulouse", "date": "2025-07-22", "tags": ["aerospace", "space", "aviation", "engineering"]},
    {"id": 60, "country": "France", "city": "Bordeaux", "date": "2025-09-12", "tags": ["wine", "vineyard", "tasting", "gastronomy"]},
    {"id": 61, "country": "France", "city": "Lille", "date": "2025-08-28", "tags": ["braderie", "festival", "market", "culture"]},
    {"id": 62, "country": "France", "city": "Nice", "date": "2025-02-15", "tags": ["carnival", "riviera", "tourism", "luxury"]},
    {"id": 63, "country": "France", "city": "Nantes", "date": "2025-05-18", "tags": ["machines", "art", "innovation", "creativity"]},
    {"id": 64, "country": "France", "city": "Strasbourg", "date": "2025-12-05", "tags": ["christmas", "market", "european", "culture"]},
    {"id": 65, "country": "France", "city": "Montpellier", "date": "2025-10-08", "tags": ["medicine", "research", "healthcare", "biotech"]},
    
    # Australia Events
    {"id": 66, "country": "Australia", "city": "Sydney", "date": "2025-01-01", "tags": ["new-year", "fireworks", "celebration", "festival"]},
    {"id": 67, "country": "Australia", "city": "Melbourne", "date": "2025-01-15", "tags": ["sports", "cricket", "tennis", "athletics"]},
    {"id": 68, "country": "Australia", "city": "Brisbane", "date": "2025-03-25", "tags": ["outdoor", "adventure", "nature", "wildlife"]},
    {"id": 69, "country": "Australia", "city": "Perth", "date": "2025-04-05", "tags": ["mining", "resources", "energy", "industry"]},
    {"id": 70, "country": "Australia", "city": "Adelaide", "date": "2025-02-20", "tags": ["wine", "festival", "food", "arts"]},
    {"id": 71, "country": "Australia", "city": "Canberra", "date": "2025-05-10", "tags": ["politics", "government", "diplomacy", "policy"]},
    {"id": 72, "country": "Australia", "city": "Gold Coast", "date": "2025-06-08", "tags": ["surfing", "beach", "sports", "tourism"]},
    {"id": 73, "country": "Australia", "city": "Newcastle", "date": "2025-07-15", "tags": ["coal", "mining", "industry", "port"]},
    {"id": 74, "country": "Australia", "city": "Wollongong", "date": "2025-08-22", "tags": ["steel", "industry", "manufacturing", "engineering"]},
    {"id": 75, "country": "Australia", "city": "Hobart", "date": "2025-09-30", "tags": ["art", "museum", "mona", "culture"]},
    
    # India Events
    {"id": 76, "country": "India", "city": "Mumbai", "date": "2025-04-25", "tags": ["bollywood", "film", "entertainment", "cinema"]},
    {"id": 77, "country": "India", "city": "Bangalore", "date": "2025-05-22", "tags": ["it", "software", "startup", "tech"]},
    {"id": 78, "country": "India", "city": "Delhi", "date": "2025-06-30", "tags": ["history", "heritage", "culture", "monuments"]},
    {"id": 79, "country": "India", "city": "Hyderabad", "date": "2025-07-10", "tags": ["pharma", "biotech", "research", "healthcare"]},
    {"id": 80, "country": "India", "city": "Chennai", "date": "2025-08-18", "tags": ["automotive", "manufacturing", "industry", "engineering"]},
    {"id": 81, "country": "India", "city": "Pune", "date": "2025-09-14", "tags": ["education", "it", "automotive", "research"]},
    {"id": 82, "country": "India", "city": "Kolkata", "date": "2025-10-28", "tags": ["literature", "book-fair", "culture", "arts"]},
    {"id": 83, "country": "India", "city": "Ahmedabad", "date": "2025-11-20", "tags": ["textile", "trade", "commerce", "industry"]},
    {"id": 84, "country": "India", "city": "Jaipur", "date": "2025-12-12", "tags": ["tourism", "heritage", "palace", "culture"]},
    {"id": 85, "country": "India", "city": "Lucknow", "date": "2025-01-25", "tags": ["food", "cuisine", "culture", "heritage"]},
    
    # UAE Events
    {"id": 86, "country": "UAE", "city": "Dubai", "date": "2025-02-05", "tags": ["luxury", "shopping", "retail", "tourism"]},
    {"id": 87, "country": "UAE", "city": "Abu Dhabi", "date": "2025-03-10", "tags": ["oil", "energy", "industry", "finance"]},
    {"id": 88, "country": "UAE", "city": "Dubai", "date": "2025-04-20", "tags": ["tech", "innovation", "startup", "expo"]},
    {"id": 89, "country": "UAE", "city": "Sharjah", "date": "2025-05-28", "tags": ["art", "culture", "heritage", "museum"]},
    {"id": 90, "country": "UAE", "city": "Dubai", "date": "2025-06-14", "tags": ["sports", "racing", "f1", "motorsports"]},
    {"id": 91, "country": "UAE", "city": "Abu Dhabi", "date": "2025-07-26", "tags": ["culture", "heritage", "history", "tradition"]},
    {"id": 92, "country": "UAE", "city": "Dubai", "date": "2025-08-30", "tags": ["food", "restaurant", "gastronomy", "dining"]},
    {"id": 93, "country": "UAE", "city": "Ajman", "date": "2025-09-18", "tags": ["manufacturing", "industry", "trade", "business"]},
    {"id": 94, "country": "UAE", "city": "Dubai", "date": "2025-10-22", "tags": ["real-estate", "property", "investment", "development"]},
    {"id": 95, "country": "UAE", "city": "Ras Al Khaimah", "date": "2025-11-25", "tags": ["tourism", "nature", "mountain", "adventure"]},
    
    # Singapore Events
    {"id": 96, "country": "Singapore", "city": "Singapore", "date": "2025-01-10", "tags": ["finance", "banking", "fintech", "trading"]},
    {"id": 97, "country": "Singapore", "city": "Singapore", "date": "2025-03-15", "tags": ["food", "hawker", "culinary", "gastronomy"]},
    {"id": 98, "country": "Singapore", "city": "Singapore", "date": "2025-05-25", "tags": ["tech", "startup", "innovation", "digital"]},
    {"id": 99, "country": "Singapore", "city": "Singapore", "date": "2025-07-28", "tags": ["shopping", "retail", "luxury", "fashion"]},
    {"id": 100, "country": "Singapore", "city": "Singapore", "date": "2025-09-22", "tags": ["education", "research", "academic", "science"]}
]

cursor.execute('SELECT * FROM events')
events_db = cursor.fetchall()

conn.close()

class add_event(BaseModel):
    country: str
    city: str
    tags: list[str]
    date: str

@app.get("/events")
async def root(id: Optional[int] = None, country: Optional[str] = None, city: Optional[str] = None, tags: Optional[list] = Query(None, description="Filter by tags")):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events')
    events_db = cursor.fetchall()
    avalible_events = events_db

    if id:
        for event in avalible_events:
            if int(event[0]) == id:
                return event
    if country:
        e = [event for event in avalible_events if event[1].lower() == country.lower()]
        avalible_events = e
    if city:
        e = [event for event in avalible_events if event[2].lower() == city.lower()]
        avalible_events = e
    if tags:
        temp = []
        for event in avalible_events:
            p = True
            for tag in tags:
                if tag not in event[4]:
                    p = False
            if p:
                temp.append(event)
                
        avalible_events = temp
    conn.close()
    return avalible_events


@app.post("/add_event/")
def add(event: add_event):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    e = (len(events_db)+1,event.country,event.city,event.date,event.tags)
    events_db.append(e)
    cursor.execute('''
    INSERT INTO events (id, country, city, date, tags)
    VALUES (?, ?, ?, ?, ?)
    ''', (e[0], e[1], e[2], 
        e[3], str(e[4])))

    # Commit the changes
    conn.commit()
    conn.close()
    return {"message":"recieved"}