#!/bin/sh

# Start the API in the background
uvicorn main:app --host 0.0.0.0 --port 8000 --log-level critical &  
API_PID=$!

# Wait for the API to be ready
echo "Waiting for API to be ready..."
while ! nc -z 0.0.0.0 8000; do  
  sleep 2
done

# Start the client
python client.py

kill "$API_PID"
