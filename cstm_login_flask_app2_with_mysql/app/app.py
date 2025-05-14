from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
from mysql.connector import Error
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management

# MySQL Connection Function
def connect_to_database():
    for i in range(10):
        try:
            db = mysql.connector.connect(
                host="db",
                user="root",
                password="root",
                database="user_db"
            )
            print("✅ Connected to database")
            cursor = db.cursor()
            return db, cursor
        except Error as e:
            print(f"❌ Attempt {i+1}: Unable to connect, retrying in 3 seconds...")
            time.sleep(3)
    raise Exception("Could not connect to the database after several attempts")

# Initialize DB and Cursor
db, cursor = connect_to_database()

# ------------------------- ROUTES -------------------------

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        session['username'] = username
        return redirect(url_for('welcome'))
    else:
        return "Invalid credentials"

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']

    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, password))
    db.commit()
    return redirect('/')

@app.route('/welcome')
def welcome():
    if 'username' in session:
        return render_template("welcome.html", username=session['username'])
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

# ------------------------- MAIN -------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)