from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "secret123"

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["flaskdb"]
users = db["users"]
grades = db["grades"]

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users.insert_one({
            "username": request.form['username'],
            "password": request.form['password']
        })
        return redirect('/login')
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = users.find_one({
            "username": request.form['username'],
            "password": request.form['password']
        })
        if user:
            session['user'] = request.form['username']
            return redirect('/dashboard')
    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', username=session['user'])
    return redirect('/login')

# View Grades
@app.route('/grades')
def view_grades():
    if 'user' in session:
        data = grades.find({"username": session['user']})
        return render_template('profile.html', grades=data)
    return redirect('/login')

# Reset Password
@app.route('/reset', methods=['GET', 'POST'])
def reset_password():
    if 'user' in session:
        if request.method == 'POST':
            users.update_one(
                {"username": session['user']},
                {"$set": {"password": request.form['password']}}
            )
            return redirect('/dashboard')
        return render_template('reset.html')
    return redirect('/login')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
