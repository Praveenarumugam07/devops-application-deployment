from flask import Flask, request, jsonify, render_template_string
import mysql.connector

app = Flask(__name__)

# MySQL database config
db_config = {
    'host': '104.155.157.238',
    'user': 'appuser',
    'password': 'Praveen@123',
    'database': 'user_management'
}

# HTML template string
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>User Management</title>
</head>
<body>
    <h1>Add User</h1>
    <form method="POST" action="/add">
        Name: <input type="text" name="name"><br>
        Age: <input type="number" name="age"><br>
        City: <input type="text" name="city"><br>
        <input type="submit" value="Add User">
    </form>
    <hr>
    <h2>All Users</h2>
    <ul>
    {% for user in users %}
        <li>{{ user[1] }} (Age: {{ user[2] }}, City: {{ user[3] }})</li>
    {% endfor %}
    </ul>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template_string(HTML_TEMPLATE, users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    age = request.form['age']
    city = request.form['city']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age, city) VALUES (%s, %s, %s)", (name, age, city))
    conn.commit()
    cursor.close()
    conn.close()
    return "User added successfully! <a href='/'>Go back</a>"

@app.route('/api/users', methods=['GET'])
def api_get_users():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
