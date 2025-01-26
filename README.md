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
    docker compose run --rm api
    ```
5. Use the Client
    - Once the services are up and running, the client will automatically start and display a prompt.
    - Available commands:
        - `query <query_text>`: Download data with the specified query.
        - `list bioassays`: List all bioassay IDs.
        - `list compounds`: List all compound IDs.
        - `bioassay <aid>`: Get a specific bioassay by its ID.
        - `compound <cid>`: Get a specific compound by its ID.
        - `drop bioassays`: Drop all bioassays.
        - `drop compounds`: Drop all compounds.
        - `drop db`:  Drop the entire database.
        - `help`: Display the list of available commands.
        - `exit`: Exit the client.
        
6. Stop the Service
   - Press `Ctrl`+`C` in your terminal to stop the running containers.

7. Remove the Service
   ```bash
   docker-compose down