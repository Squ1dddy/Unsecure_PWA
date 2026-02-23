import sqlite3 as sql
import time
import random
import bcrypt


def insertUser(username, password, DoB):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    # HASHING AND SALT STEPS
    encoded_password = password.encode("utf-8")
    hashed_pass = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    hashed_string = hashed_pass.decode("utf-8")
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)",
        (username, hashed_string, DoB),
    )
    con.commit()
    con.close()


def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()


    cur.execute("SELECT password FROM users WHERE username == ?", (username,))
    row = cur.fetchone()

    if row is None:
        con.close()
        return False
    else:
        stored_hash_string = row[0]
        stored_hash = stored_hash_string.encode("utf-8")
        encoded_pass = password.encode("utf-8")
        
        password_matches = bcrypt.checkpw(encoded_pass, stored_hash)

        # Plain text log of visitor count as requested by Unsecure PWA management
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        con.close()
        return password_matches


def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO feedback (feedback) VALUES ('{feedback}')")
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()
