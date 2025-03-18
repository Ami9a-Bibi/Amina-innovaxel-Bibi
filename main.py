from fastapi import FastAPI, HTTPException, Body, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
import random
import string

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./shortener.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# URL Model
class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    shortCode = Column(String, unique=True, index=True, nullable=False)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
    visit_count = Column(Integer, default=0)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic model for URL requests
class URLRequest(BaseModel):
    url: str

# Generate a random short code
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Shorten URL
@app.post("/shorten", status_code=status.HTTP_201_CREATED)
def shorten_url(request: URLRequest):
    db = SessionLocal()
    short_code = generate_short_code()
    
    # Ensure short code uniqueness
    while db.query(URL).filter(URL.shortCode == short_code).first():
        short_code = generate_short_code()

    new_url = URL(url=request.url, shortCode=short_code)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    db.close()

    return {
        "id": new_url.id,
        "url": new_url.url,
        "shortCode": new_url.shortCode,
        "createdAt": new_url.createdAt,
        "updatedAt": new_url.updatedAt,
    }

# Retrieve original URL and increment visit count
@app.get("/{short_code}")
def get_original_url(short_code: str):
    db = SessionLocal()
    url_entry = db.query(URL).filter(URL.shortCode == short_code).first()

    if not url_entry:
        db.close()
        raise HTTPException(status_code=404, detail="Not Found")

    url_entry.visit_count += 1
    db.commit()
    db.refresh(url_entry)
    db.close()

    return {"id": url_entry.id,
        "url": url_entry.url,
        "shortCode": url_entry.shortCode,
        "createdAt": url_entry.createdAt,
        "updatedAt": url_entry.updatedAt,}

# Get URL stats (visit count)
@app.get("/stats/{short_code}")
def get_url_stats(short_code: str):
    db = SessionLocal()
    url_entry = db.query(URL).filter(URL.shortCode == short_code).first()
    db.close()

    if not url_entry:
        raise HTTPException(status_code=404, detail="Not Found")

    return {   "id": url_entry.id,
        "url": url_entry.url,
        "shortCode": url_entry.shortCode,
        "createdAt": url_entry.createdAt,
        "updatedAt": url_entry.updatedAt,
        "accessCount": url_entry.visit_count}

# Update an existing short URL
@app.put("/shorten/{short_code}")
def update_short_url(short_code: str, url: str = Body(..., embed=True)):
    db = SessionLocal()
    url_entry = db.query(URL).filter(URL.shortCode == short_code).first()

    if not url_entry:
        db.close()
        raise HTTPException(status_code=404, detail="Not Found")

    url_entry.url = url
    db.commit()
    db.refresh(url_entry)
    db.close()

    return {
        "id": url_entry.id,
        "url": url_entry.url,
        "shortCode": url_entry.shortCode,
        "createdAt": url_entry.createdAt,
        "updatedAt": url_entry.updatedAt
    }

# Delete a short URL
@app.delete("/shorten/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_short_url(short_code: str):
    db = SessionLocal()
    url_entry = db.query(URL).filter(URL.shortCode == short_code).first()
    
    if not url_entry:
        db.close()
        raise HTTPException(status_code=404, detail="Not Found")

    db.delete(url_entry)
    db.commit()
    db.close()

    return {"message": "Short URL deleted successfully"}
