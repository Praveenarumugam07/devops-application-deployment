import pyodbc

DATABASE_CONFIG = {
    'server': '/cloudsql/sylvan-hydra-464904-d9:us-central1:my-app-db',
    'database': 'user_management',
    'username': 'appuser',
    'password': 'Praveen@123',
    'driver': '{ODBC Driver 17 for SQL Server}'
}

try:
    conn = pyodbc.connect(
        f"DRIVER={DATABASE_CONFIG['driver']};"
        f"SERVER={DATABASE_CONFIG['server']};"
        f"DATABASE={DATABASE_CONFIG['database']};"
        f"UID={DATABASE_CONFIG['username']};"
        f"PWD={DATABASE_CONFIG['password']};"
        "Encrypt=no;"
    )
    print("✅ Database Connection Successful!")
except Exception as e:
    print(f"❌ Database Connection Failed: {e}")
