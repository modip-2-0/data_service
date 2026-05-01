# Data Service API

A FastAPI-based service for downloading and managing bioassay and compound data from PubChem.

## Collaborators

- ScM Dany Naranjo Feliciano
- ScM Romel Calero Ramos
- BEng Sandy Chávez Rodríguez

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
- `GET /bioassay/get/{aid}` - Get a specific bioassay by its ID

### Compounds
- `GET /compound/` - List all compounds
- `POST /compound/insert` - Create new compound
- `GET /compound/get/{cid}` - Get a specific compound by its ID

### Download Engine
- `POST /download/{query}` - Download bioassays and compounds matching query

## Setup

1. Install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/linux/)

2. Clone the repository

    ```bash
    git clone https://github.com/modip-2-0/data_service.git
    cd data_service
    ```

3. Build the Service

    ```bash
    docker compose build 
    ```
4. Start the Service

    ```bash
    docker compose up data_service
    ```
        
6. Stop the Service
   - Press `Ctrl`+`C` in your terminal to stop the running containers.

7. Remove the Service
   ```bash
   docker compose down
