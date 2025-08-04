FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for pyodbc and MySQL
RUN apt-get update && apt-get install -y \
    gcc g++ unixodbc-dev \
    default-libmysqlclient-dev \
    curl gnupg \
    && rm -rf /var/lib/apt/lists/*

# For ODBC Driver (SQL Server support)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full application
COPY . .

# Expose port (optional)
EXPOSE 8080

# Default command
CMD ["python", "app.py"]
