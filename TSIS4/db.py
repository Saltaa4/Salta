# db.py
import psycopg2
from psycopg2 import sql


DB_CONFIG = {
    "dbname":   "snake_game",
    "user":     "postgres",
    "password": "pg12345678",
    "host":     "localhost",
    "port":     5432,
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    """Create tables if they don't exist."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id       SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id            SERIAL PRIMARY KEY,
                    player_id     INTEGER REFERENCES players(id),
                    score         INTEGER   NOT NULL,
                    level_reached INTEGER   NOT NULL,
                    played_at     TIMESTAMP DEFAULT NOW()
                );
            """)
        conn.commit()


def get_or_create_player(username: str) -> int:
    """Return player id, creating the row if needed."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM players WHERE username = %s", (username,))
            row = cur.fetchone()
            if row:
                return row[0]
            cur.execute(
                "INSERT INTO players (username) VALUES (%s) RETURNING id",
                (username,)
            )
            player_id = cur.fetchone()[0]
        conn.commit()
    return player_id


def save_session(username: str, score: int, level_reached: int):
    """Save a finished game session."""
    player_id = get_or_create_player(username)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO game_sessions (player_id, score, level_reached)
                VALUES (%s, %s, %s)
                """,
                (player_id, score, level_reached)
            )
        conn.commit()


def get_leaderboard(limit: int = 10):
    """Return top scores: list of (rank, username, score, level, date_str)."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.username, gs.score, gs.level_reached,
                       TO_CHAR(gs.played_at, 'DD.MM.YY') AS played_at
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                ORDER BY gs.score DESC
                LIMIT %s
            """, (limit,))
            rows = cur.fetchall()
    return [(i + 1, *row) for i, row in enumerate(rows)]


def get_personal_best(username: str) -> int:
    """Return the player's all-time best score, or 0 if none."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COALESCE(MAX(gs.score), 0)
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                WHERE p.username = %s
            """, (username,))
            return cur.fetchone()[0]