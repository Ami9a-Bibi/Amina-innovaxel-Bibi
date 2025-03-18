from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel
import random
import string

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./shortener.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    shortCode = Column(String, unique=True, index=True, nullable=False)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
    visit_count = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

class URLRequest(BaseModel):
    url: str

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.post("/shorten")
def shorten_url(request: URLRequest):
    db = SessionLocal()
    short_code = generate_short_code()
    
    # Commit 5: Generate unique short codes
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
