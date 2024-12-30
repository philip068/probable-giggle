import sqlite3
from typing import List,Tuple, Any
from db_utils import db_cursor, fetch_id_mapping
from logger import get_logger
from topic_priority import TopicPriority
from frequency_weights import FrequencyWeights

logger = get_logger(__name__, 'add_problems.log')

def associate_entries(
    cursor: sqlite3.Cursor,
    table: str,
    columns: Tuple[str, str],
    entries: List[Tuple[int, int]]
) -> None:
    """Bulk insert associations into a many-to-many table."""
    cursor.executemany(f'''
        INSERT OR IGNORE INTO {table} ({columns[0]}, {columns[1]})
        VALUES (?, ?)
    ''', entries)
    logger.info(f"Inserted {cursor.rowcount} entries into the {table} table.")

def compute_priority(topic: str, frequency: str) -> int:
    """Compute final priority based on topic and frequency weights."""
    base_priority = TopicPriority.get_priority(topic)
    freq_weight = FrequencyWeights.get_weight(frequency)
    computed_priority = max(1, base_priority // freq_weight)
    logger.debug(f"Computed priority for topic '{topic}' with frequency '{frequency}': {computed_priority}")
    return computed_priority

def validate_prerequisites(cursor: sqlite3.Cursor, prereq_ids: List[int]) -> List[int]:
    """Validate prerequisite IDs to ensure they exist in the Problems table."""
    if not prereq_ids:
        return []
    placeholders = ','.join(['?'] * len(prereq_ids))
    query = f'SELECT id FROM Problems WHERE id IN ({placeholders})'
    cursor.execute(query, prereq_ids)
    valid_ids = {row['id'] for row in cursor.fetchall()}
    missing_ids = set(prereq_ids) - valid_ids
    if missing_ids:
        logger.warning(f"Missing prerequisite IDs: {missing_ids}. They will be skipped.")
    return list(valid_ids)

def resolve_prerequisites(cursor: sqlite3.Cursor, problems: List[Tuple]):
    """
    Resolve prerequisites for problems after initial insertion.
    
    Parameters:
        cursor (sqlite3.Cursor): The database cursor.
        problems (List[Tuple]): The list of problems to process.
    
    Returns:
        None
    """
    unresolved_prereqs = []
    for problem in problems:
        if len(problem) != 8:
            logger.error(f"Invalid problem tuple: {problem}")
            continue
        problem_id, _, _, _, _, _, _, prereqs = problem
        if prereqs:
            valid_prereq_ids = validate_prerequisites(cursor, prereqs)
            if valid_prereq_ids:
                associate_entries(
                    cursor,
                    'ProblemPrerequisites',
                    ('problem_id', 'prerequisite_id'),
                    [(problem_id, pid) for pid in valid_prereq_ids]
                )
                logger.info(f"Resolved prerequisites for problem ID={problem_id}: {valid_prereq_ids}")
            else:
                unresolved_prereqs.append((problem_id, prereqs))

    if unresolved_prereqs:
        logger.warning("Some prerequisites could not be resolved after all insertions:")
        for problem_id, prereqs in unresolved_prereqs:
            logger.warning(f"  Problem ID={problem_id} has unresolved prerequisites: {prereqs}")

def insert_problems(cursor: sqlite3.Cursor, problems: List[Tuple[Any, ...]]) -> None:
    """Bulk insert problems into the Problems table."""
    cursor.executemany('''
        INSERT OR IGNORE INTO Problems (
            id, title, difficulty, topic_id, url, priority, frequency
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', problems)
    logger.info(f"Inserted {cursor.rowcount} problems into the Problems table.")

def add_problems(problems: List[Tuple], db_path: str = 'leetcode_mastery.db') -> None:
    """Add a list of problems to the database with improved prerequisite handling."""
    with db_cursor(db_path) as cursor:
        # Pre-fetch mappings
        topic_mapping = fetch_id_mapping(cursor, 'Topics', 'name')
        pattern_mapping = fetch_id_mapping(cursor, 'Patterns', 'name')

        problems_to_insert = []
        problem_patterns_entries = []

        for problem in problems:
            if len(problem) != 8:
                logger.error(f"Invalid problem tuple: {problem}")
                continue
            try:
                problem_id, title, difficulty, topic, patterns, url, frequency, prereqs = problem

                # Validate topic
                topic_id = topic_mapping.get(topic)
                if not topic_id:
                    logger.error(f"Missing topic '{topic}' for problem '{title}' (ID={problem_id}). Skipping.")
                    continue

                # Compute priority
                priority = compute_priority(topic, frequency)

                # Add problem for insertion
                problems_to_insert.append((problem_id, title, difficulty, topic_id, url, priority, frequency))

                # Add patterns for association
                valid_pattern_ids = [pattern_mapping.get(p) for p in patterns if pattern_mapping.get(p)]
                problem_patterns_entries.extend([(problem_id, pid) for pid in valid_pattern_ids])

            except Exception as e:
                logger.error(f"Error processing problem '{title}' (ID={problem_id}): {e}")

        # Insert problems and patterns
        if problems_to_insert:
            insert_problems(cursor, problems_to_insert)

        if problem_patterns_entries:
            associate_entries(cursor, 'ProblemPatterns', ('problem_id', 'pattern_id'), problem_patterns_entries)

        # Resolve prerequisites after all problems have been inserted
        resolve_prerequisites(cursor, problems)

        logger.info(f"Successfully added {len(problems_to_insert)} problems to the database.")

if __name__ == "__main__":
    from sample_problems import sample_problems  # Ensure this module exists and contains sample_problems
    add_problems(sample_problems)
