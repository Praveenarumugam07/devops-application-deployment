FROM python:3.10-slim-bullseye

ENV ACCEPT_EULA=Y
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and ODBC drivers
RUN apt-get update && \
    apt-get install -y curl gnupg2 apt-transport-https software-properties-common && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev gcc g++ && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN python -m pip install --upgrade pip && \
    pip install flask mysql-connector-python bcrypt pyodbc

# Optional: verify pyodbc is installed
RUN python -c "import pyodbc"

# Copy application code
COPY . /app
WORKDIR /app

# Run the app
CMD ["python", "app.py"]
