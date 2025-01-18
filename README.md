# Data Service API

A FastAPI-based service for downloading and managing bioassay and compound data from PubChem.

## Features

- Download bioassays and compounds from PubChem based on search queries
- Store data in MongoDB database
- RESTful API endpoints for data access and management
- Asynchronous operations for improved performance

## Architecture

- `api/` - API routes and dependencies
- `core/` - Core configurations and database setup
- `crud/` - Database operations
- `download_engine/` - PubChem data download logic
- `models/` - Pydantic data models

## API Endpoints

### Bioassays
- `GET /bioassay/` - List all bioassays
- `POST /bioassay/insert` - Create new bioassay

### Compounds
- `GET /compound/` - List all compounds
- `POST /compound/insert` - Create new compound

### Download Engine
- `POST /download/{query}` - Download bioassays and compounds matching query

## Setup

1. Install MongoDB locally
2. Configure MongoDB connection in `core/db.py`
3. Install dependencies
4. Run FastAPI application

## Dependencies

- FastAPI
- Motor (async MongoDB driver)
- Pydantic
- Requests



## Usage

Start the server:

```bash
uvicorn api.main:app --reload
```

Access API documentation at: `http://localhost:8000/docs`