from flask import Flask, render_template, request, redirect, url_for
import pyodbc  # Use pyodbc instead of mysql.connector
import bcrypt  
from config import DATABASE_CONFIG

app = Flask(__name__)

# Microsoft SQL Server configurations (Cloud SQL Public IP: 35.192.101.149)
DATABASE_CONFIG = {
    'server': 'vamsidb.c9uqkcqc8c92.ap-south-1.rds.amazonaws.com',  # Public IP of your Cloud SQL MSSQL instance
    'database': 'test01',  # Change to your database name
    'username': 'admin',  # MSSQL username
    'password': 'Svamsi79955',  # MSSQL password
    'driver': '{ODBC Driver 17 for SQL Server}'  # Ensure this driver is installed
}

# Establish Connection to MSSQL
try:
    conn = pyodbc.connect(
        f"DRIVER={DATABASE_CONFIG['driver']};"
        f"SERVER={DATABASE_CONFIG['server']};"
        f"DATABASE={DATABASE_CONFIG['database']};"
        f"UID={DATABASE_CONFIG['username']};"
        f"PWD={DATABASE_CONFIG['password']};"
        "TrustServerCertificate=yes"
    )
    cursor = conn.cursor()
    print("✅ Connected to MSSQL successfully!")

    # Create a table to store user data if it doesn't exist
    create_table_query = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='user' AND xtype='U')
        CREATE TABLE [user] (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(255),
            email NVARCHAR(255),
            Address NVARCHAR(MAX),
            phonenumber NVARCHAR(255),
            password NVARCHAR(255)
        )
    """
    cursor.execute(create_table_query)
    conn.commit()
except Exception as e:
    print(f"❌ Database Connection Failed: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        phonenumber = request.form['phonenumber']
        
        # Hash the password before storing it
        password = request.form['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        # Insert user data into the database
        insert_query = "INSERT INTO [user] (name, email, Address, phonenumber, password) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(insert_query, (name, email, address, phonenumber, hashed_password))
        conn.commit()
        
        # Fetch the latest entry
        cursor.execute("SELECT * FROM [user] ORDER BY id DESC")
        data = cursor.fetchall()

        return render_template('submitteddata.html', data=data)
    
    return redirect(url_for('index'))

@app.route('/get-data', methods=['GET', 'POST'])
def get_data():
    if request.method == 'POST':
        # Retrieve data based on user input ID
        input_id = request.form['input_id']
        select_query = "SELECT * FROM [user] WHERE id = ?"
        cursor.execute(select_query, (input_id,))
        data = cursor.fetchall()
        return render_template('data.html', data=data, input_id=input_id)
    return render_template('get_data.html')

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_data(id):
    if request.method == 'POST':
        # Perform deletion based on the provided ID
        delete_query = "DELETE FROM [user] WHERE id = ?"
        cursor.execute(delete_query, (id,))
        conn.commit()
        return redirect(url_for('get_data'))
    return render_template('delete.html', id=id)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
