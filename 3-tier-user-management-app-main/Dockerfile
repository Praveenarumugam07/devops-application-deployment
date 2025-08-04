FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for mysql-connector
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Expose port
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]
