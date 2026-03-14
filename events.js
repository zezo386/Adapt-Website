const API_URL = 'https://events-api-production-4a05.up.railway.app/events';

const searchInput = document.getElementById('search');
const locationFilter = document.getElementById('location-filter');
const dateFilter = document.getElementById('date-filter');
const tagFilter = document.getElementById('tag-filter');
const applyFiltersBtn = document.getElementById('apply-filters');
const resetFiltersBtn = document.getElementById('reset-filters');
const eventsContainer = document.getElementById('events');

all_events = [];
filtered_events = [];

async function get_events(){
    try{
        response = await fetch(API_URL)
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const events = await response.json();
        return events;
    }
    catch (error){
        console.error("an error occured",error)
        return null
    }
}

function convertArrayToEvent(eventArray) {
    // Check if it's an array and has the right structure
    if (!Array.isArray(eventArray) || eventArray.length < 5) {
        console.error('Invalid event array:', eventArray);
        return null;
    }
    
    // Parse tags - remove brackets and quotes, split by commas
    let tags = [];
    if (eventArray[4] && typeof eventArray[4] === 'string') {
        // Remove [ and ] and ' characters, then split by comma
        const tagsString = eventArray[4].replace(/[\[\]']/g, '');
        tags = tagsString.split(',').map(tag => tag.trim()).filter(tag => tag);
    }
    
    return {
        id: eventArray[0],
        country: eventArray[1],
        city: eventArray[2],
        date: eventArray[3],
        tags: tags,
        title: eventArray[5],
        description: eventArray[6]
    };
}

function processTags(tagsString) {
    if (!tagsString) return [];
    
    // Remove brackets and quotes, then split by commas
    const cleaned = tagsString.replace(/[\[\]']/g, '');
    return cleaned.split(',').map(tag => tag.trim()).filter(tag => tag);
}

function add_event_card(event){
    const event_date = new Date(event.date)
    const formatteddate = event_date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    })

    tagsHTML = event.tags && event.tags.length > 0 ? event.tags.map(tag => `<span class="event-tag">${tag}</span>`).join(''): ''
    return `
    <div class="event-card" onclick="handleEventClick(${event.id})">
        <div class="card-title">
            <h2 class="card-title">${event.title}</h2>
            <span class="card-date">${formatteddate}</span>
        </div>
        <div class="card-location">location: ${event.city}, ${event.country}</div>
        <div class="card-description">${event.description}</div>
        ${tagsHTML ? `<div class="event-tags">${tagsHTML}</div>` : ''}
        <div class="card-footer">
            <span class="card-id">event #${event.id}</span>
        </div>
    </div>
    
    `

}


function handleEventClick(event){
    console.log(`event #${event} clicked`)
}


async function displayEvents() {
    const container = document.getElementById('events');
    
    // Show loading state
    container.innerHTML = '<div class="loading">Loading events...</div>';
    
    // Fetch events
    const events = await get_events();
    
    if (!events) {
        container.innerHTML = '<div class="error">Failed to load events. Please try again later.</div>';
        return;
    }
    
    all_events = events.map(event => convertArrayToEvent(event));
    console.log(all_events)
    

    if (all_events.length === 0) {
        container.innerHTML = '<div class="error">No events found.</div>';
        return;
    }

    filter_events();

    // Set filtered events to all events initially
    filtered_events = [...all_events];
    
    // Create and insert event cards
    const eventsHTML = filtered_events.map(event => add_event_card(event)).join('');
    container.innerHTML = eventsHTML;
    
    // Initialize filters after events are loaded
    initFilters();
}



function filter_events(){
    const locations = [...new Set(all_events.map(event => event.country))].sort();
    const allTags = [];
    all_events.forEach(event => {
        event.tags.forEach(tag => {
            if (!allTags.includes(tag)) allTags.push(tag);
        });
    });
    allTags.sort();

    if (locationFilter){
        locationFilter.innerHTML = '<option value="all">All Locations</option>';
        console.log(locations)
        locations.forEach(location => {locationFilter.innerHTML += `<option value="${location.toLowerCase()}">${location}</option>`;});
    }

    if (tagFilter){
        tagFilter.innerHTML = '<option value="all">All Tags</option>';
        allTags.forEach(tag => {tagFilter.innerHTML += `<option value="${tag.toLowerCase()}">${tag}</option>`;});
    }

    if (dateFilter) {
        dateFilter.innerHTML = `
            <option value="all">All Dates</option>
            <option value="today">Today</option>
            <option value="tomorrow">Tomorrow</option>
            <option value="week">This Week</option>
            <option value="weekend">This Weekend</option>
            <option value="month">This Month</option>
            <option value="next-month">Next Month</option>
        `;
    }
}

function initFilters() {
    if (searchInput) {
        searchInput.addEventListener('input', debounce(ApplyFilters, 300));
    }
    
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', ApplyFilters);
    }
    
    if (resetFiltersBtn) {
        resetFiltersBtn.addEventListener('click', resetFilters);
    }
}

function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}


function ApplyFilters(){
    const searchTerm = searchInput?.value.toLowerCase().trim() || '';
    const location = locationFilter?.value || 'all';
    const date = dateFilter?.value || 'all';
    const tag = tagFilter?.value || 'all';
    
    filteredEvents = all_events.filter(event => {
        // Search filter
        if (searchTerm) {
            const titleMatch = event.title.toLowerCase().includes(searchTerm);
            const locationMatch = `${event.city} ${event.country}`.toLowerCase().includes(searchTerm);
            const descriptionMatch = event.description.toLowerCase().includes(searchTerm);
            const tagsMatch = event.tags.some(tag => tag.toLowerCase().includes(searchTerm));
            
            if (!titleMatch && !locationMatch && !descriptionMatch && !tagsMatch) {
                return false;
            }
        }
        
        // Location filter
        if (location !== 'all') {
            const eventLocation = `${event.city} ${event.country}`.toLowerCase();
            if (!eventLocation.includes(location.toLowerCase())) {
                return false;
            }
        }
        
        // Tag filter
        if (tag !== 'all') {
            if (!event.tags.some(t => t.toLowerCase() === tag.toLowerCase())) {
                return false;
            }
        }
        
        // Date filter
        if (date !== 'all') {
            if (!matchesDateFilter(event.date, date)) {
                return false;
            }
        }
        
        return true;
    });
    
    updateDisplay();

}

function matchesDateFilter(event_date_str, filter) {
    const event_date = new Date(event_date_str);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    const nextWeek = new Date(today);
    nextWeek.setDate(nextWeek.getDate() + 7);
    
    const nextMonth = new Date(today);
    nextMonth.setMonth(nextMonth.getMonth() + 1);
    
    const endMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0);
    
    switch(filter) {
        case 'today':
            return event_date.toDateString() === today.toDateString();
            
        case 'tomorrow':
            return event_date.toDateString() === tomorrow.toDateString();
            
        case 'week':
            return event_date >= today && event_date <= nextWeek;
            
        case 'weekend':
            const day = event_date.getDay();
            return (day === 5 || day === 6) && event_date >= today;
            
        case 'month':
            return event_date.getMonth() === today.getMonth() && 
                   event_date.getFullYear() === today.getFullYear() &&
                   event_date >= today;
            
        case 'next-month':
            return event_date.getMonth() === (today.getMonth() + 1) % 12 &&
                   event_date.getFullYear() >= today.getFullYear();
            
        default:
            return true;
    }
}

function resetFilters() {
    if (searchInput) searchInput.value = '';
    if (locationFilter) locationFilter.value = '';
    if (dateFilter) dateFilter.value = '';
    if (tagFilter) tagFilter.value = '';
    
    filteredEvents = [...all_events];
    displayEvents(filteredEvents);
    updateResultsCount();
}

function updateDisplay() {
    const container = document.getElementById('events');
    
    if (filteredEvents.length === 0) {
        container.innerHTML = `
            <div class="no-results">
                <i class="fas fa-search"></i>
                <h3>No events found</h3>
                <p>Try adjusting your filters or search term</p>
                <button onclick="resetFilters()" class="reset-btn">
                    <i class="fas fa-undo"></i> Reset Filters
                </button>
            </div>
        `;
        return;
    }
    
    const eventsHTML = filteredEvents.map(event => add_event_card(event)).join('');
    container.innerHTML = eventsHTML;
}


const style = document.createElement('style');
style.textContent = `
    .no-results {
        grid-column: 1 / -1;
        text-align: center;
        padding: 60px;
        background: white;
        border-radius: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.02);
    }
    
    .no-results i {
        font-size: 3rem;
        color: #94a3b8;
        margin-bottom: 20px;
    }
    
    .no-results h3 {
        font-size: 1.5rem;
        color: #1e293b;
        margin-bottom: 10px;
    }
    
    .no-results p {
        color: #64748b;
        margin-bottom: 30px;
    }
    
    .reset-btn {
        background: #3b82f6;
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 40px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .reset-btn:hover {
        background: #2563eb;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(59, 130, 246, 0.2);
    }
`;
document.head.appendChild(style);


function initNavbar() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navMenu = document.getElementById('navMenu');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }

    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
        });
    });

    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
}
document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    displayEvents();
});




