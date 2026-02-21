from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["flaskdb"]
grades = db["grades"]

grades.delete_many({})

grades.insert_many([
    {"username": "partho", "subject": "Maths", "marks": 85},
    {"username": "partho", "subject": "Physics", "marks": 78},
    {"username": "partho", "subject": "DBMS", "marks": 90},
    {"username": "partho", "subject": "Signal", "marks": 70},
    {"username": "partho", "subject": "OS", "marks": 70}
])

print("Sample data inserted")