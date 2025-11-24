from fastapi import FastAPI
import secrets
from datetime import datetime

app = FastAPI()

# Simple in-memory storage
url_database = {}

@app.get("/")
def home():
    return {
        "message": "URL Shortener API", 
        "endpoints": {
            "shorten": "GET /shorten?url=URL",
            "redirect": "GET /go/:code", 
            "stats": "GET /stats",
            "health": "GET /health"
        }
    }

@app.get("/shorten")
def shorten_url(url: str):
    """Shorten a URL"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    code = secrets.token_urlsafe(6)
    url_database[code] = {
        "original_url": url,
        "short_code": code,
        "created_at": datetime.now().isoformat(),
        "visits": 0
    }
    return {
        "short_url": f"http://localhost:8000/go/{code}",
        "code": code,
        "original_url": url
    }

@app.get("/go/{code}")
def redirect_url(code: str):
    """Redirect to original URL (simulated)"""
    if code in url_database:
        url_database[code]["visits"] += 1
        return {
            "action": "redirect",
            "to": url_database[code]["original_url"],
            "visits": url_database[code]["visits"]
        }
    return {"error": "URL not found"}

@app.get("/stats")
def get_stats():
    """Get statistics"""
    total_visits = sum(url["visits"] for url in url_database.values())
    return {
        "total_urls": len(url_database),
        "total_visits": total_visits,
        "urls": list(url_database.keys())
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
