# FastAPI URL Shortener

This is a simple URL shortener API built using FastAPI and SQLite. It allows users to shorten URLs, retrieve original URLs, track access statistics, update existing URLs, and delete short URLs.

## Features
- Shorten a given URL
- Retrieve the original URL using the short code
- Track the number of times a short URL has been accessed
- Update an existing short URL
- Delete a short URL

## Installation

### Prerequisites
- Python 3.8+
- Git
- SQLite (comes pre-installed with Python)

### Steps
1. **Clone the repository:**
   ```sh
   git clone https://github.com/Ami9a-Bibi/Amina-innovaxel-Bibi.git
   cd Amina-innovaxel-Bibi
   ```
2. **Switch to the `dev` branch:**
   ```sh
   git checkout dev
   ```
3. **Create a virtual environment (optional but recommended):**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
4. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Running the API
Start the FastAPI server using Uvicorn:
```sh
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### 1. Shorten URL
**POST** `/shorten`
#### Request Body:
```json
{
  "url": "https://example.com"
}
```
#### Response:
```json
{
  "id": 1,
  "url": "https://example.com",
  "shortCode": "abc123",
  "createdAt": "2025-03-18T12:00:00",
  "updatedAt": "2025-03-18T12:00:00"
}
```

### 2. Retrieve Original URL
**GET** `/{short_code}`
#### Response:
```json
{
  "id": 1,
  "url": "https://example.com",
  "shortCode": "abc123",
  "createdAt": "2025-03-18T12:00:00",
  "updatedAt": "2025-03-18T12:00:00"
}
```

### 3. Get URL Statistics
**GET** `/stats/{short_code}`
#### Response:
```json
{
  "id": 1,
  "url": "https://example.com",
  "shortCode": "abc123",
  "createdAt": "2025-03-18T12:00:00",
  "updatedAt": "2025-03-18T12:00:00",
  "accessCount": 5
}
```

### 4. Update Short URL
**PUT** `/shorten/{short_code}`
#### Request Body:
```json
{
  "url": "https://newexample.com"
}
```
#### Response:
```json
{
  "id": 1,
  "url": "https://newexample.com",
  "shortCode": "abc123",
  "createdAt": "2025-03-18T12:00:00",
  "updatedAt": "2025-03-18T12:10:00"
}
```

### 5. Delete Short URL
**DELETE** `/shorten/{short_code}`
#### Response:
```json
{
  "message": "Short URL deleted successfully"
}
```

