
# Use a lightweight Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependencies and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# Create the folder used for database storage
RUN mkdir -p /app/data

# Flask application port
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
