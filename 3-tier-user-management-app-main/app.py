from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import bcrypt

app = Flask(__name__)

# Database configuration for MySQL on GCP
DATABASE_CONFIG = {
    'host': '104.155.157.238',          # GCP SQL instance public IP
    'user': 'appuser',                  # DB username
    'password': 'Praveen@123',   # Replace with actual password
    'database': 'user_management'       # DB name
}

# Function to establish DB connection
def get_connection():
    try:
        conn = mysql.connector.connect(
            host=DATABASE_CONFIG['host'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            database=DATABASE_CONFIG['database']
        )
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
        return None

# Initialize DB table if not exists
conn = get_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            address TEXT,
            phonenumber VARCHAR(20),
            password VARCHAR(255)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    conn = get_connection()
    if not conn:
        return "Database connection failed", 500

    cursor = conn.cursor()
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']
    phonenumber = request.form['phonenumber']
    
    password = request.form['password'].encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    insert_query = """
        INSERT INTO users (name, email, address, phonenumber, password)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (name, email, address, phonenumber, hashed_password))
    conn.commit()

    cursor.execute("SELECT * FROM users ORDER BY id DESC")
    data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('submitteddata.html', data=data)

@app.route('/get-data', methods=['GET', 'POST'])
def get_data():
    if request.method == 'POST':
        input_id = request.form['input_id']
        conn = get_connection()
        if not conn:
            return "Database connection failed", 500

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (input_id,))
        data = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return render_template('data.html', data=data, input_id=input_id)
    return render_template('get_data.html')

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_data(id):
    if request.method == 'POST':
        conn = get_connection()
        if not conn:
            return "Database connection failed", 500

        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        return redirect(url_for('get_data'))
    return render_template('delete.html', id=id)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
