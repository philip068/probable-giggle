import sqlite3
from contextlib import contextmanager
from typing import Generator, Dict, Any
from logger import get_logger

logger = get_logger(__name__, 'database.log')

@contextmanager
def db_cursor(db_path: str) -> Generator[sqlite3.Cursor, None, None]:
    """
    Context manager for SQLite database cursor.
    
    Parameters:
        db_path (str): Path to the SQLite database file.
    
    Yields:
        sqlite3.Cursor: Database cursor object.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON;')
        cursor = conn.cursor()
        yield cursor
        conn.commit()
        logger.debug("Transaction committed successfully.")
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
            logger.error(f"Transaction rolled back due to error: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logger.debug(f"Database connection to '{db_path}' closed.")

def fetch_id_mapping(cursor: sqlite3.Cursor, table: str, column: str) -> Dict[str, int]:
    """
    Fetch a mapping from a specific column to its corresponding ID.
    
    Parameters:
        cursor (sqlite3.Cursor): Database cursor.
        table (str): Table name.
        column (str): Column name to map.
    
    Returns:
        Dict[str, int]: Mapping from column value to ID.
    """
    singular_table = table.rstrip('s').lower()  # e.g., 'Topics' -> 'topic'
    id_column = f"{singular_table}_id"
    cursor.execute(f"SELECT {id_column}, {column} FROM {table}")
    rows = cursor.fetchall()
    return {row[column]: row[id_column] for row in rows}
