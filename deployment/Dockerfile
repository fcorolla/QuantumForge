# Use FastAPI base image with Python
FROM python:3.12

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend files
COPY backend/src/ /app/

# Set up entry point for API server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]