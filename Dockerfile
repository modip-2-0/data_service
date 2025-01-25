# Use the base image with Python 3.12
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install netcat
RUN apt-get update && apt-get install -y netcat-openbsd    

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# Copy the rest of the application code
COPY . .

# Ensure the start.sh script is executable
RUN chmod +x start.sh

# Expose the port the API will run on
EXPOSE 8000

# # Set the default command to run the start.sh script
# CMD ["./start.sh"]