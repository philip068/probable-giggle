import sqlite3
import matplotlib.pyplot as plt
import datetime
import logging
from contextlib import contextmanager
from typing import List, Tuple, Any, Optional
import argparse
from logger import get_logger

logger = get_logger(__name__, 'visualize_progress.log')

def get_connection(db_path: str = 'leetcode_mastery.db') -> sqlite3.Connection:
    """
    Establish a connection to the SQLite database.

    Parameters:
        db_path (str): Path to the SQLite database file.

    Returns:
        sqlite3.Connection: SQLite connection object.
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        logger.debug(f"Connected to database at '{db_path}'.")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise

def plot_graph(x: List[Any], y: List[float], title: str, xlabel: str, ylabel: str, kind: str = 'line', save_path: Optional[str] = None) -> None:
    """
    Utility function to plot graphs.

    Parameters:
        x (List[Any]): Data for the x-axis.
        y (List[float]): Data for the y-axis.
        title (str): Title of the plot.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        kind (str): Type of plot ('line' or 'bar'). Default is 'line'.
        save_path (Optional[str]): Path to save the plot image. If None, displays the plot.
    """
    plt.figure(figsize=(10, 6))

    if kind == 'line':
        plt.plot(x, y, marker='o', linestyle='-', color='blue')
    elif kind == 'bar':
        plt.bar(x, y, color='skyblue')
    else:
        logger.warning(f"Unsupported plot kind '{kind}'. Defaulting to 'line'.")
        plt.plot(x, y, marker='o', linestyle='-', color='blue')

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        logger.info(f"Plot saved to {save_path}")
    else:
        plt.show()

def fetch_data(query: str, params: Tuple = (), db_path: str = 'leetcode_mastery.db') -> List[sqlite3.Row]:
    """
    Fetch data from the database.

    Parameters:
        query (str): SQL query to execute.
        params (Tuple): Parameters for the SQL query.
        db_path (str): Path to the SQLite database file.

    Returns:
        List[sqlite3.Row]: List of rows fetched from the database.
    """
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            logger.debug(f"Fetched {len(rows)} rows for query: {query}")
            return rows
    except sqlite3.Error as e:
        logger.error(f"Database query error: {e}")
        return []

def plot_success_over_time(db_path: str, save_path: Optional[str] = None) -> None:
    """
    Plot the success rate over time.

    Parameters:
        db_path (str): Path to the SQLite database file.
        save_path (Optional[str]): Path to save the plot image.
    """
    query = '''
        SELECT last_attempt, SUM(successes) as successes, SUM(attempts) as attempts
        FROM UserProgress
        WHERE last_attempt IS NOT NULL
        GROUP BY last_attempt
        ORDER BY last_attempt
    '''
    rows = fetch_data(query, db_path=db_path)

    dates, rates = [], []
    for row in rows:
        try:
            date = datetime.datetime.strptime(row['last_attempt'], "%Y-%m-%dT%H:%M:%S").date()
            success_rate = (row['successes'] / row['attempts']) * 100 if row['attempts'] else 0
            dates.append(date)
            rates.append(success_rate)
        except Exception as e:
            logger.warning(f"Skipping invalid data: {e}")

    if dates and rates:
        plot_graph(dates, rates, "Success Rate Over Time", "Date", "Success Rate (%)", kind='line', save_path=save_path)
    else:
        logger.info("No data available to plot for Success Rate Over Time.")

def plot_mastered_topics(db_path: str, save_path: Optional[str] = None) -> None:
    """
    Plot the number of mastered problems by topic.

    Parameters:
        db_path (str): Path to the SQLite database file.
        save_path (Optional[str]): Path to save the plot image.
    """
    query = '''
        SELECT t.name as topic, COUNT(p.id) as total, SUM(up.mastered) as mastered
        FROM Problems p
        JOIN Topics t ON p.topic_id = t.topic_id
        LEFT JOIN UserProgress up ON p.id = up.problem_id
        GROUP BY t.name
    '''
    rows = fetch_data(query, db_path=db_path)

    topics, mastered_counts = [], []
    for row in rows:
        topics.append(row['topic'])
        mastered_counts.append(row['mastered'] or 0)

    if topics and mastered_counts:
        plot_graph(topics, mastered_counts, "Mastered Problems by Topic", "Topic", "Number of Mastered Problems", kind='bar', save_path=save_path)
    else:
        logger.info("No data available to plot for Mastered Problems by Topic.")

def plot_difficulty_success(db_path: str, save_path: Optional[str] = None) -> None:
    """
    Plot the success rate categorized by difficulty.

    Parameters:
        db_path (str): Path to the SQLite database file.
        save_path (Optional[str]): Path to save the plot image.
    """
    query = '''
        SELECT p.difficulty, SUM(up.successes) as successes, SUM(up.attempts) as attempts
        FROM Problems p
        LEFT JOIN UserProgress up ON p.id = up.problem_id
        GROUP BY p.difficulty
    '''
    rows = fetch_data(query, db_path=db_path)

    difficulties, success_rates = [], []
    for row in rows:
        difficulties.append(row['difficulty'])
        rate = (row['successes'] / row['attempts'] * 100) if row['attempts'] and row['attempts'] > 0 else 0
        success_rates.append(rate)

    if difficulties and success_rates:
        plot_graph(difficulties, success_rates, "Success Rate by Difficulty", "Difficulty", "Success Rate (%)", kind='bar', save_path=save_path)
    else:
        logger.info("No data available to plot for Success Rate by Difficulty.")
        

def main():
    parser = argparse.ArgumentParser(description="Visualize progress metrics.")
    parser.add_argument('--db-path', default='leetcode_mastery.db', help='Path to the SQLite database file.')
    parser.add_argument('--save', help='Path to save the plot image (optional).')
    parser.add_argument('--type', required=True, choices=['time', 'topics', 'difficulty'],
                        help='Type of plot to generate: time (success over time), topics (mastered by topic), difficulty (success by difficulty).')

    args = parser.parse_args()

    if args.type == 'time':
        plot_success_over_time(args.db_path, save_path=args.save)
    elif args.type == 'topics':
        plot_mastered_topics(args.db_path, save_path=args.save)
    elif args.type == 'difficulty':
        plot_difficulty_success(args.db_path, save_path=args.save)

if __name__ == "__main__":
    main()
