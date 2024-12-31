import sqlite3
from prettytable import PrettyTable
import logging
import json
from typing import List, Dict, Any, Optional
from logger import get_logger

logger = get_logger(__name__, 'view_progress.log')

def fetch_overall_metrics(cursor: sqlite3.Cursor) -> Dict[str, Any]:
    """
    Fetch overall progress metrics.

    Parameters:
        cursor (sqlite3.Cursor): Database cursor.

    Returns:
        Dict[str, Any]: Dictionary containing overall metrics.
    """
    metrics: Dict[str, Any] = {}

    cursor.execute('SELECT COUNT(*) FROM Problems')
    metrics['total_problems'] = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM UserProgress')
    metrics['attempted_problems'] = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM UserProgress WHERE mastered = 1')
    metrics['mastered'] = cursor.fetchone()[0]

    cursor.execute('SELECT SUM(attempts) FROM UserProgress')
    metrics['total_attempts'] = cursor.fetchone()[0] or 0

    cursor.execute('SELECT SUM(successes) FROM UserProgress')
    metrics['total_successes'] = cursor.fetchone()[0] or 0

    metrics['success_rate'] = (
        (metrics['total_successes'] / metrics['total_attempts'] * 100)
        if metrics['total_attempts'] > 0 else 0
    )

    logger.debug(f"Overall Metrics: {metrics}")
    return metrics

def fetch_progress_by_difficulty(cursor: sqlite3.Cursor) -> List[Dict[str, Any]]:
    """
    Fetch progress metrics categorized by difficulty.

    Parameters:
        cursor (sqlite3.Cursor): Database cursor.

    Returns:
        List[Dict[str, Any]]: List of metrics per difficulty level.
    """
    cursor.execute('SELECT DISTINCT difficulty FROM Problems')
    difficulties = [row[0] for row in cursor.fetchall()]
    
    progress: List[Dict[str, Any]] = []
    for difficulty in difficulties:
        cursor.execute('''
            SELECT COUNT(*) FROM UserProgress up
            JOIN Problems p ON up.problem_id = p.id
            WHERE p.difficulty = ?
        ''', (difficulty,))
        attempted = cursor.fetchone()[0]

        cursor.execute('''
            SELECT COUNT(*) FROM UserProgress up
            JOIN Problems p ON up.problem_id = p.id
            WHERE p.difficulty = ? AND up.mastered = 1
        ''', (difficulty,))
        mastered_count = cursor.fetchone()[0]

        cursor.execute('''
            SELECT SUM(up.successes) FROM UserProgress up
            JOIN Problems p ON up.problem_id = p.id
            WHERE p.difficulty = ?
        ''', (difficulty,))
        successes = cursor.fetchone()[0] or 0

        cursor.execute('''
            SELECT SUM(up.attempts) FROM UserProgress up
            JOIN Problems p ON up.problem_id = p.id
            WHERE p.difficulty = ?
        ''', (difficulty,))
        attempts = cursor.fetchone()[0] or 0

        diff_success_rate = (successes / attempts * 100) if attempts > 0 else 0
        progress.append({
            "difficulty": difficulty,
            "attempted": attempted,
            "mastered": mastered_count,
            "success_rate": round(diff_success_rate, 2)
        })
        logger.debug(f"Difficulty '{difficulty}': {progress[-1]}")
    return progress

def fetch_progress_by_topic(cursor: sqlite3.Cursor) -> List[Dict[str, Any]]:
    """
    Fetch progress metrics categorized by topic.

    Parameters:
        cursor (sqlite3.Cursor): Database cursor.

    Returns:
        List[Dict[str, Any]]: List of metrics per topic.
    """
    cursor.execute('''
        SELECT t.name AS topic, COUNT(p.id) AS total,
               SUM(CASE WHEN up.mastered = 1 THEN 1 ELSE 0 END) AS mastered
        FROM Problems p
        JOIN Topics t ON p.topic_id = t.topic_id
        LEFT JOIN UserProgress up ON p.id = up.problem_id
        GROUP BY t.name
    ''')
    results = cursor.fetchall()
    progress = [{
        "topic": row["topic"],
        "total": row["total"],
        "mastered": row["mastered"] or 0
    } for row in results]
    logger.debug(f"Progress by Topic: {progress}")
    return progress

def render_table(data: List[Dict[str, Any]], field_names: List[str]) -> None:
    """
    Render data as a pretty table.

    Parameters:
        data (List[Dict[str, Any]]): List of dictionaries containing data.
        field_names (List[str]): List of field names for table headers.
    """
    table = PrettyTable()
    table.field_names = field_names
    for entry in data:
        table.add_row(entry.values())
    print(table)

def render_json(data: Any) -> None:
    """
    Render data as JSON.

    Parameters:
        data (Any): Data to be rendered as JSON.
    """
    print(json.dumps(data, indent=4))

def view_progress(db_path: str = 'leetcode_mastery.db', output_format: str = 'table') -> None:
    """
    Display overall progress metrics, progress by difficulty, and progress by topic.

    Parameters:
        db_path (str): Path to the SQLite database file.
        output_format (str): Format of the output - table or JSON.
    """
    logger.info(f"Viewing progress from database '{db_path}' with format '{output_format}'.")

    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Overall Metrics
            metrics = fetch_overall_metrics(cursor)
            print("Overall Progress:")
            if output_format.lower() == 'json':
                render_json(metrics)
            else:
                table = PrettyTable()
                table.field_names = ["Total Problems", "Attempted Problems", "Mastered", "Success Rate (%)"]
                table.add_row([
                    metrics['total_problems'],
                    metrics['attempted_problems'],
                    metrics['mastered'],
                    round(metrics['success_rate'], 2)
                ])
                print(table)
            print()

            # Progress by Difficulty
            print("Progress by Difficulty:")
            progress_difficulty = fetch_progress_by_difficulty(cursor)
            if output_format.lower() == 'json':
                render_json(progress_difficulty)
            else:
                render_table(progress_difficulty, ["Difficulty", "Attempted", "Mastered", "Success Rate (%)"])
            print()

            # Progress by Topic
            print("Progress by Topic:")
            progress_topic = fetch_progress_by_topic(cursor)
            if output_format.lower() == 'json':
                render_json(progress_topic)
            else:
                render_table(progress_topic, ["Topic", "Total Problems", "Mastered"])
            print()

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        print("⚠️ An error occurred while fetching progress metrics.")
    except Exception as ex:
        logger.error(f"Unexpected error: {ex}")
        print("⚠️ An unexpected error occurred while fetching progress metrics.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="View progress metrics.")
    parser.add_argument('--db-path', default='leetcode_mastery.db', help='Path to the SQLite database file.')
    parser.add_argument('--output-format', default='table', choices=['table', 'json'],
                        help='Output format: table (default) or JSON.')
    args = parser.parse_args()

    view_progress(db_path=args.db_path, output_format=args.output_format)
