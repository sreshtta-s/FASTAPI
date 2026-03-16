from fastapi import FastAPI
import mysql.connector
import json

app = FastAPI()

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root123",
    port=3307,
    database="api_database"
)

cursor = db.cursor()

@app.post("/add_user")
def add_user(data: dict):

    personal = data["personalDetails"]
    hobby = data["hobby"]
    reading = data["reading"]
    family = data["familyBackground"]

    firstName = personal["firstName"]
    middleName = personal["middleName"]

    # DUPLICATE CHECK
    cursor.execute(
        "SELECT * FROM users WHERE firstName=%s AND middleName=%s",
        (firstName, middleName)
    )

    existing = cursor.fetchone()

    if existing:
        return {"message": "Duplicate user found"}

    # INSERT DATA
    query = """
    INSERT INTO users
    (
        firstName,
        middleName,
        lastName,
        age,
        occupation,
        gameName,
        isHeWatchMovie,
        isHeTarvel,
        isHeReadBooks,
        favBooks,
        familyBackground
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        personal["firstName"],
        personal["middleName"],
        personal["lastName"],
        personal["age"],
        personal["occupation"],
        hobby["gameName"],
        hobby["isHeWatchMovie"],
        hobby["isHeTarvel"],
        reading["isHeReadBooks"],
        reading["favBooks"],
        json.dumps(family)
    )

    cursor.execute(query, values)
    db.commit()

    return {"message": "User inserted successfully"}