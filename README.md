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

1. Install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/linux/)

2. Clone the repository

    ```bash
    git clone https://github.com/modip-2-0/data_service.git
    cd data_service
    ```

3. Start the Service

    ```bash
    docker compose up | grep -v mongo
    ```

   -  This command will start the services while filtering out MongoDB logs for a cleaner output.
   
   
   

4. Access the FastAPI Documentation
    - Open your web browser and go to http://0.0.0.0:8000/docs to view the interactive API documentation.
    - Testing Endpoints:
        - Select the desired endpoint.
        - Click "Try it out".
        - If it's a POST request, provide the necessary request body in JSON format.
        - Click "Execute" to send the request and view the response.

5. Direct Database Access (Not Recommended):
    - Important:  It is generally recommended to use the provided API for data interaction. Direct database queries bypass application logic and can potentially lead to data inconsistencies or security vulnerabilities.
    - If you want to access the database directly, open a new terminal and execute the following command:
      
    ```bash
    docker exec -it data_service-mongodb-1 mongosh
    ```
    - This command launches the MongoDB shell (mongosh) within the running MongoDB container.
    - Basic MongoDB Commands: Once in the shell, you can execute commands to interact with the database. Here are a few examples:
    ```javascript
    > use modip       // Switch to the 'modip' database.
    > show collections // List available collections.
    > db.bioassays.find() // Retrieve documents from the 'bioassays' collection.
    > db.compounds.find() // Retrieve documents from the 'compounds' collection.
    ```
6. Stop the Service
   - Press `Ctrl`+`C` in your terminal to stop the running containers.

7. Remove the Service
   ```bash
   docker compose down
   ```
   
   - This command will stop and remove the containers, networks, and volumes created by `docker compose up`.