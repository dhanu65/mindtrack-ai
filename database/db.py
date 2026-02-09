import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("database/emotions.db")
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Emotion history per user
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emotion_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            text TEXT,
            emotion TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def register_user(username, password):
    conn = sqlite3.connect("database/emotions.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        success = True
    except:
        success = False

    conn.close()
    return success


def login_user(username, password):
    conn = sqlite3.connect("database/emotions.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    return user is not None


def save_result(user, text, emotion):
    conn = sqlite3.connect("database/emotions.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO emotion_history (user, text, emotion) VALUES (?, ?, ?)",
        (user, text, emotion)
    )

    conn.commit()
    conn.close()


def get_history(user):
    conn = sqlite3.connect("database/emotions.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT text, emotion FROM emotion_history WHERE user=?",
        (user,)
    )

    rows = cursor.fetchall()
    conn.close()
    return rows
