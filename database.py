import sqlite3
from config import DATABASE_FILE
from database.models import CREATE_PLAYERS_TABLE


def get_connection():
    return sqlite3.connect(DATABASE_FILE)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(CREATE_PLAYERS_TABLE)
    conn.commit()
    conn.close()


def get_player(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id, current_scene, state_json, is_over FROM players WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row


def upsert_player(user_id: int, current_scene: str, state_json: str, is_over: int):
    conn = get_connection()
    cursor = conn.cursor()

    existing = get_player(user_id)
    if existing:
        cursor.execute(
            """
            UPDATE players
            SET current_scene = ?, state_json = ?, is_over = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            """,
            (current_scene, state_json, is_over, user_id)
        )
    else:
        cursor.execute(
            """
            INSERT INTO players (user_id, current_scene, state_json, is_over)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, current_scene, state_json, is_over)
        )

    conn.commit()
    conn.close()


def reset_player(user_id: int, current_scene: str, state_json: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players WHERE user_id = ?", (user_id,))
    cursor.execute(
        """
        INSERT INTO players (user_id, current_scene, state_json, is_over)
        VALUES (?, ?, ?, 0)
        """,
        (user_id, current_scene, state_json)
    )
    conn.commit()
    conn.close()
