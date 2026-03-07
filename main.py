from fastapi import FastAPI,Query,HTTPException, Depends, Header
from typing import Optional
from pydantic import BaseModel
import sqlite3
import json
from datetime import datetime, timedelta
import secrets

conn = sqlite3.connect('events.db')
cursor = conn.cursor()


app = FastAPI()


events_db = []

cursor.execute('SELECT * FROM events')
events_db = cursor.fetchall()
cursor.execute("DELETE FROM events WHERE date < ?",(datetime.now().date().strftime('%Y-%m-%d'), ))

conn.commit()

conn.close()



def verify_api_key(api_key):
    
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    
    # First, check and reset daily counters if needed
    cursor.execute('''
        SELECT id, daily_limit, requests_today, last_reset_date, name 
        FROM api_keys 
        WHERE key = ? AND is_active = 1
    ''', (api_key,))
    
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid or inactive API key")
    
    key_id, daily_limit, requests_today, last_reset_date, key_name = row
    
    # Check if we need to reset the daily counter (new day)
    today = datetime.now().date()
    last_reset = datetime.strptime(last_reset_date, '%Y-%m-%d').date()
    
    if today > last_reset:
        # Reset counter for new day
        cursor.execute('''
            UPDATE api_keys 
            SET requests_today = 0, last_reset_date = ? 
            WHERE id = ?
        ''', (today, key_id))
        requests_today = 0
    
    # Check if key has exceeded daily limit
    if requests_today >= daily_limit:
        conn.close()
        raise HTTPException(
            status_code=429,  # Too Many Requests
            detail=f"Daily API limit of {daily_limit} requests exceeded. Please try again tomorrow."
        )
    
    # Increment the request counter
    cursor.execute('''
        UPDATE api_keys 
        SET requests_today = requests_today + 1,
            last_used = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (key_id,))
    
    conn.commit()
    conn.close()
    
    return True , key_id, key_name

class add_event(BaseModel):
    country: str
    city: str
    tags: list[str]
    date: str
    api_key: str

@app.get("/events")
async def root(id: Optional[int] = None, country: Optional[str] = None, city: Optional[str] = None, tags: Optional[list] = Query(None, description="Filter by tags"), date: Optional[str] = None):
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
    
    if date:
        temp = [event for event in avalible_events if event[3]>date]
        avalible_events = temp

    conn.close()
    return avalible_events


@app.post("/add_event/")
def add(
    event: add_event, 
):

    
    # Verify the API key
    is_valid, key_id, key_name = verify_api_key(event.api_key)
    
    if not is_valid:
        raise HTTPException(
            status_code=401, 
            detail="Invalid or inactive API key"
        )
    
    # If key is valid, proceed with adding the event
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    
    try:
        # Insert the event
        cursor.execute('''
        INSERT INTO events (country, city, date, tags)
        VALUES (?, ?, ?, ?)
        ''', (event.country, event.city, event.date, str(event.tags)))
        
        # Get the auto-generated ID
        event_id = cursor.lastrowid
        
        # Commit the changes
        conn.commit()
        
        return {
            "message": "Event added successfully",
            "event_id": event_id,
            "used_by": key_name  # Show which API key was used
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()