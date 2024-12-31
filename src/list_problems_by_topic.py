import sqlite3
from prettytable import PrettyTable
import click
import logging
import json
from typing import List, Dict, Any, Optional
from logger import get_logger

logger = get_logger(__name__, 'list_problems_by_topic.log')

def fetch_topic_id(cursor: sqlite3.Cursor, topic: str) -> Optional[int]:
    """
    Fetch the topic ID for a given topic name.

    Parameters:
        cursor (sqlite3.Cursor): Database cursor.
        topic (str): The name of the topic.

    Returns:
        Optional[int]: The topic ID if found, else None.
    """
    query = 'SELECT topic_id FROM Topics WHERE name = ? COLLATE NOCASE'
    cursor.execute(query, (topic,))
    topic_row = cursor.fetchone()
    if topic_row:
        logger.debug(f"Found topic ID {topic_row['topic_id']} for topic '{topic}'.")
        return topic_row['topic_id']
    else:
        logger.warning(f"Topic '{topic}' not found in the database.")
        return None

def fetch_problems_by_topic(cursor: sqlite3.Cursor, topic_id: int) -> List[Dict[str, Any]]:
    """
    Fetch problems for a given topic ID.

    Parameters:
        cursor (sqlite3.Cursor): Database cursor.
        topic_id (int): The ID of the topic.

    Returns:
        List[Dict[str, Any]]: List of problems associated with the topic.
    """
    query = '''
        SELECT p.id, p.title, p.difficulty, t.name AS topic, 
               GROUP_CONCAT(pr.name, ', ') AS patterns, 
               p.frequency, p.url
        FROM Problems p
        JOIN Topics t ON p.topic_id = t.topic_id
        LEFT JOIN ProblemPatterns pp ON p.id = pp.problem_id
        LEFT JOIN Patterns pr ON pp.pattern_id = pr.pattern_id
        WHERE t.topic_id = ?
        GROUP BY p.id
        ORDER BY p.priority ASC, 
                 CASE p.difficulty 
                     WHEN 'Easy' THEN 1 
                     WHEN 'Medium' THEN 2 
                     WHEN 'Hard' THEN 3 
                     ELSE 4 
                 END ASC
    '''
    cursor.execute(query, (topic_id,))
    problems = cursor.fetchall()
    logger.info(f"Fetched {len(problems)} problems for topic ID {topic_id}.")
    return [dict(problem) for problem in problems]

def render_table(problems: List[Dict[str, Any]]) -> PrettyTable:
    """
    Render problems as a pretty table.

    Parameters:
        problems (List[Dict[str, Any]]): List of problem dictionaries.

    Returns:
        PrettyTable: The rendered table.
    """
    table = PrettyTable()
    table.field_names = ["ID", "Title", "Difficulty", "Topic", "Patterns", "Frequency", "URL"]
    for row in problems:
        table.add_row([
            row['id'],
            row['title'],
            row['difficulty'],
            row['topic'],
            row['patterns'] if row['patterns'] else "None",
            row['frequency'],
            row['url']
        ])
    return table

def render_json(problems: List[Dict[str, Any]]) -> str:
    """
    Render problems as JSON.

    Parameters:
        problems (List[Dict[str, Any]]): List of problem dictionaries.

    Returns:
        str: JSON string of problems.
    """
    return json.dumps(problems, indent=4)

def get_problems_by_topic(topic: str, db_path: str = 'leetcode_mastery.db', output_format: str = 'table') -> None:
    """
    Core function to get and render problems by topic.

    Parameters:
        topic (str): The name of the topic to filter by.
        db_path (str): Path to the SQLite database file.
        output_format (str): Format of the output - table or JSON.
    """
    logger.info(f"Listing problems for topic '{topic}' from database '{db_path}' with format '{output_format}'.")

    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Fetch topic ID
            topic_id = fetch_topic_id(cursor, topic)
            if topic_id is None:
                click.echo(f"❌ Topic '{topic}' does not exist in the database.")
                return

            # Fetch problems
            problems = fetch_problems_by_topic(cursor, topic_id)
            if not problems:
                click.echo(f"ℹ️ No problems found for topic: {topic}")
                return

            # Render output
            if output_format.lower() == 'table':
                table = render_table(problems)
                print(table)
            elif output_format.lower() == 'json':
                json_output = render_json(problems)
                print(json_output)

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        click.echo("⚠️ An error occurred while listing problems by topic.")
    except Exception as ex:
        logger.error(f"Unexpected error: {ex}")
        click.echo("⚠️ An unexpected error occurred while listing problems by topic.")

@click.command()
@click.option('--topic', prompt='Topic Name', type=str, help='Topic to filter problems by.')
@click.option('--db-path', default='leetcode_mastery.db', show_default=True, help='Path to the SQLite database file.')
@click.option('--output-format', default='table', type=click.Choice(['table', 'json'], case_sensitive=False),
              show_default=True, help='Output format: table (default) or JSON.')
def list_problems_by_topic_cli(topic: str, db_path: str, output_format: str) -> None:
    """
    Click command to list problems by topic.
    """
    get_problems_by_topic(topic, db_path, output_format)

if __name__ == "__main__":
    list_problems_by_topic_cli()
