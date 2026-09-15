import sqlite3
import json

DATABASE_NAME = "flashcards.db"


def create_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cards TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_deck(name, cards):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO decks (name, cards) VALUES (?, ?)",
        (name, json.dumps(cards))
    )

    conn.commit()
    conn.close()


def get_decks():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM decks")
    decks = cursor.fetchall()

    conn.close()

    return decks


def load_deck(deck_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, cards FROM decks WHERE id = ?",
        (deck_id,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        name, cards = result
        return name, json.loads(cards)

    return None, []


def delete_deck(deck_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM decks WHERE id = ?",
        (deck_id,)
    )

    conn.commit()
    conn.close()