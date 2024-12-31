import argparse
import sys
import sqlite3
from typing import List, Tuple

from logger import get_logger
from db_utils import db_cursor

logger = get_logger(__name__, 'db_init.log')

def drop_tables(cursor: sqlite3.Cursor) -> None:
    """
    Drops existing tables if they exist.
    
    Parameters:
        cursor (sqlite3.Cursor): Database cursor.
    """
    tables = [
        'UserProgress', 'ProblemPatterns', 'TopicRatings',
        'Problems', 'Topics', 'Patterns', 'ProblemPrerequisites'
    ]
    cursor.execute('PRAGMA foreign_keys = OFF;')
    for table in tables:
        cursor.execute(f'DROP TABLE IF EXISTS {table}')
        logger.info(f"Dropped table '{table}' if it existed.")
    cursor.execute('PRAGMA foreign_keys = ON;')
    logger.debug("Foreign key constraints re-enabled.")

def create_tables(cursor: sqlite3.Cursor) -> None:
    """
    Creates necessary tables if they do not exist.
    
    Parameters:
        cursor (sqlite3.Cursor): Database cursor.
    """
    tables_sql = {
        "Topics": '''CREATE TABLE IF NOT EXISTS Topics (
            topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )''',
        "Patterns": '''CREATE TABLE IF NOT EXISTS Patterns (
            pattern_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )''',
        "Problems": '''CREATE TABLE IF NOT EXISTS Problems (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            topic_id INTEGER NOT NULL,
            url TEXT NOT NULL,
            priority INTEGER NOT NULL DEFAULT 100,
            frequency TEXT NOT NULL DEFAULT 'Medium',
            FOREIGN KEY (topic_id) REFERENCES Topics(topic_id)
        )''',
        "ProblemPrerequisites": '''CREATE TABLE IF NOT EXISTS ProblemPrerequisites (
            problem_id INTEGER,
            prerequisite_id INTEGER,
            FOREIGN KEY (problem_id) REFERENCES Problems(id),
            FOREIGN KEY (prerequisite_id) REFERENCES Problems(id),
            PRIMARY KEY (problem_id, prerequisite_id)
        )''',
        "UserProgress": '''CREATE TABLE IF NOT EXISTS UserProgress (
            problem_id INTEGER PRIMARY KEY,
            attempts INTEGER DEFAULT 0,
            successes INTEGER DEFAULT 0,
            hints_used INTEGER DEFAULT 0,
            time_spent INTEGER DEFAULT 0,
            last_attempt DATETIME,
            next_due DATETIME,
            mastered INTEGER DEFAULT 0 NOT NULL,
            current_interval_index INTEGER DEFAULT 0,
            FOREIGN KEY (problem_id) REFERENCES Problems(id)
        )''',
        "TopicRatings": '''CREATE TABLE IF NOT EXISTS TopicRatings (
            topic_id INTEGER PRIMARY KEY,
            rating REAL DEFAULT 1500,
            FOREIGN KEY (topic_id) REFERENCES Topics(topic_id)
        )''',
        "ProblemPatterns": '''CREATE TABLE IF NOT EXISTS ProblemPatterns (
            problem_id INTEGER,
            pattern_id INTEGER,
            FOREIGN KEY (problem_id) REFERENCES Problems(id),
            FOREIGN KEY (pattern_id) REFERENCES Patterns(pattern_id),
            PRIMARY KEY (problem_id, pattern_id)
        )'''
    }

    for table, sql in tables_sql.items():
        cursor.execute(sql)
        logger.info(f"Ensured table '{table}' exists.")

    indexes = [
        'CREATE INDEX IF NOT EXISTS idx_problems_topic_id ON Problems(topic_id)',
        'CREATE INDEX IF NOT EXISTS idx_problempatterns_problem_id ON ProblemPatterns(problem_id)',
        'CREATE INDEX IF NOT EXISTS idx_problempatterns_pattern_id ON ProblemPatterns(pattern_id)',
        'CREATE INDEX IF NOT EXISTS idx_problemprerequisites_prerequisite_id ON ProblemPrerequisites(prerequisite_id)',
        'CREATE INDEX IF NOT EXISTS idx_userprogress_mastered ON UserProgress(mastered)'
    ]
    for index in indexes:
        cursor.execute(index)
        logger.info(f"Ensured index '{index}' exists.")

    logger.info("Created necessary tables and indexes.")

def initialize_table(cursor: sqlite3.Cursor, table: str, data: List[str], column_name: str) -> None:
    """
    Generic function to initialize a table with predefined data.
    
    Parameters:
        cursor (sqlite3.Cursor): Database cursor.
        table (str): Name of the table to initialize.
        data (List[str]): List of data entries to insert.
        column_name (str): Column name for insertion.
    """
    records: List[Tuple[str]] = [(item,) for item in data]
    cursor.executemany(f'INSERT OR IGNORE INTO {table} ({column_name}) VALUES (?)', records)
    logger.info(f"Initialized '{table}' table with predefined data.")

def initialize_topic_ratings(cursor: sqlite3.Cursor) -> None:
    """
    Initializes TopicRatings based on Topics table.
    
    Parameters:
        cursor (sqlite3.Cursor): Database cursor.
    """
    cursor.execute('SELECT topic_id FROM Topics')
    topics: List[Tuple[int]] = cursor.fetchall()
    records: List[Tuple[int, float]] = [(topic_id, 1500.0) for (topic_id,) in topics]
    cursor.executemany('''
        INSERT OR IGNORE INTO TopicRatings (topic_id, rating)
        VALUES (?, ?)
    ''', records)
    logger.info("Initialized 'TopicRatings' based on 'Topics' table.")

def initialize_db(reset: bool = False, db_path: str = 'leetcode_mastery.db') -> None:
    """
    Initialize (or optionally reset) the leetcode_mastery.db database.
    
    Parameters:
        reset (bool): If True, drops existing tables before creating new ones.
        db_path (str): Path to the SQLite database file.
    """
    topics = [
        "Array", "String", "Linked List", "Hash Table", "Stack",
        "Queue", "Tree", "Binary Tree", "Binary Search Tree",
        "Graph", "Heap", "Dynamic Programming", "Greedy",
        "Backtracking", "Bit Manipulation", "Trie", "Union-Find",
        "Segment Tree", "Topological Sort", "Binary Search",
        "Sorting", "Math", "Database"
    ]
    patterns = [
        "Two Pointers", "Sliding Window", "Recursion", "Iteration",
        "Divide and Conquer", "Math", "Top-Down DP", "Bottom-Up DP",
        "Memoization", "Tabulation", "K-Way Partitioning", "Randomization",
        "Branch and Bound", "Parallel Algorithms", "Trie", "Union-Find", "Stack", "Queue",
        "Dynamic Programming", "Hash Table", "Heap", "Depth-First Search",
        "Breadth-First Search", "Greedy", "Backtracking", "Bit Manipulation",
        "Topological Sort", "Binary Search", "Sorting", "Simulation", "Design"
    ]

    with db_cursor(db_path) as cursor:
        if reset:
            drop_tables(cursor)
        create_tables(cursor)
        initialize_table(cursor, 'Topics', topics, 'name')
        initialize_table(cursor, 'Patterns', patterns, 'name')
        initialize_topic_ratings(cursor)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize the LeetCode Mastery database.")
    parser.add_argument('--reset', action='store_true', help='Reset the database by dropping existing tables.')
    parser.add_argument('--db_path', type=str, default='leetcode_mastery.db', help='Path to the SQLite database file.')
    args = parser.parse_args()

    if args.reset:
        confirmation = input("Are you sure you want to reset the database? This will erase all existing data. (yes/no): ")
        if confirmation.lower() != 'yes':
            print("Database reset canceled.")
            sys.exit(0)

    try:
        initialize_db(reset=args.reset, db_path=args.db_path)
        logger.info("Database initialization completed successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize the database: {e}")
        sys.exit(1)
