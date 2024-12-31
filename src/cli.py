import csv
import json
import math
import click
import sqlite3
import datetime
import webbrowser
from prettytable import PrettyTable
import logging
from contextlib import contextmanager
from typing import Generator, Optional, List

from scheduler import ProblemScheduler
from models import Problem
from prerequisite_map import PREREQUISITE_MAP
from topic_priority import TopicPriority
from list_problems_by_topic import get_problems_by_topic
from utils import prompt_positive_int
from logger import get_logger

DIFFICULTY_ORDER = {'Easy': 1, 'Medium': 2, 'Hard': 3}

logger = get_logger(__name__, 'cli.log')

@click.group()
def cli():
    """Advanced LeetCode Mastery CLI"""
    pass


@cli.command()
def reset() -> None:
    """
    Reset the entire database (all tables dropped) or just progress.
    """
    confirm = click.confirm("Are you sure you want to reset all data? This will drop all tables. Type 'yes' to confirm.", default=False)
    if confirm:
        try:
            import db_init
            db_init.initialize_db(reset=True)
            click.echo("Database has been reset. All tables dropped and re-created.")
            logger.info("Database has been reset by the user.")
        except ImportError as e:
            logger.error(f"Failed to import db_init module: {e}")
            click.echo("⚠️ Failed to reset the database due to internal error.")
        except Exception as e:
            logger.error(f"Error in reset command: {e}")
            click.echo(f"⚠️ An error occurred while resetting the database: {e}")
    else:
        click.echo("Reset action canceled.")

@cli.group()
def problem():
    """Commands related to problem management."""
    pass

@problem.command(name='add')
@click.option('--id', prompt='Problem ID', type=int, help='LeetCode Problem ID')
@click.option('--title', prompt='Title', type=str, help='Problem Title')
@click.option('--difficulty', prompt='Difficulty (Easy/Medium/Hard)', type=click.Choice(['Easy', 'Medium', 'Hard'], case_sensitive=False), help='Problem Difficulty')
@click.option('--topic', prompt='Topic', type=str, help='Problem Topic')
@click.option('--patterns', prompt='Patterns (comma-separated)', type=str, help='Problem Patterns')
@click.option('--url', prompt='URL', type=str, help='Problem URL')
@click.option('--frequency', prompt='Frequency (High/Medium/Low)', type=click.Choice(['High', 'Medium', 'Low'], case_sensitive=False), help='Interview Frequency')
@click.option('--prerequisites', prompt='Prerequisite Problem IDs (comma-separated)', default='', help='Comma-separated Problem IDs')
def add_problem(
    id: int,
    title: str,
    difficulty: str,
    topic: str,
    patterns: str,
    url: str,
    frequency: str,
    prerequisites: str
) -> None:
    """
    Add a new problem to the database.
    
    Parameters:
        id (int): LeetCode Problem ID.
        title (str): Problem Title.
        difficulty (str): Problem Difficulty.
        topic (str): Problem Topic.
        patterns (str): Comma-separated Problem Patterns.
        url (str): Problem URL.
        frequency (str): Interview Frequency.
        prerequisites (str): Comma-separated Prerequisite Problem IDs.
    """
    logger.info(f"Attempting to add problem ID {id}: '{title}'")
    try:
        import add_problems
        prereq_list = [int(pid.strip()) for pid in prerequisites.split(',') if pid.strip().isdigit()] if prerequisites else []
        patterns_list = [p.strip() for p in patterns.split(',')] if patterns else []
        add_problems.add_problems([(id, title, difficulty.capitalize(), topic, patterns_list, url, frequency.capitalize(), prereq_list)])
        click.echo(f"Problem '{title}' added successfully.")
        logger.info(f"Successfully added problem ID {id}: '{title}'")
    except ImportError as e:
        logger.error(f"Failed to import add_problems module: {e}")
        click.echo("⚠️ Failed to add problem due to internal error.")
    except ValueError as e:
        logger.error(f"Invalid input format: {e}")
        click.echo("⚠️ Invalid input format. Please ensure prerequisites are numeric IDs.")
    except Exception as e:
        logger.error(f"Error in add command: {e}")
        click.echo(f"⚠️ An error occurred while adding the problem: {e}")


@problem.command(name='list')
@click.option('--difficulty', type=click.Choice(['Easy', 'Medium', 'Hard'], case_sensitive=False), default=None, help='Filter by difficulty.')
@click.option('--topic', default=None, help='Filter by topic (supports partial matching).')
@click.option('--pattern', default=None, help='Filter by pattern (supports partial matching).')
@click.option('--page', type=int, default=1, help='Page number for paginated results.')
@click.option('--per-page', type=int, default=10, help='Number of results per page.')
@click.option('--verbose', is_flag=True, help='Show detailed output (default).')
@click.option('--compact', is_flag=True, help='Show compact output with minimal columns.')
def list_problems(difficulty: Optional[str], topic: Optional[str], pattern: Optional[str], page: int, per_page: int, verbose: bool, compact: bool) -> None:
    """
    List problems in the database with enhanced input validation, pagination, and flexible output modes.

    Usage Examples:
        list
        list --difficulty Easy
        list --topic string
        list --pattern Two
        list --page 2 --per-page 5
        list --difficulty medium --topic array
        list --difficulty medium --verbose
        list --difficulty medium --compact
    """
    try:
        scheduler = ProblemScheduler()
        with scheduler.get_connection() as conn:
            cursor = conn.cursor()

            # Base query
            query = '''
                SELECT p.id, p.title, p.difficulty, t.name AS topic, 
                       GROUP_CONCAT(pr.name, ', ') AS patterns, 
                       p.url, p.priority, p.frequency, 
                       GROUP_CONCAT(pp2.prerequisite_id, ',') AS prerequisites
                FROM Problems p
                JOIN Topics t ON p.topic_id = t.topic_id
                LEFT JOIN ProblemPatterns pp ON p.id = pp.problem_id
                LEFT JOIN Patterns pr ON pp.pattern_id = pr.pattern_id
                LEFT JOIN ProblemPrerequisites pp2 ON p.id = pp2.problem_id
            '''
            conditions = []
            params = []

            # Add filters with enhanced input validation
            if difficulty:
                conditions.append("LOWER(p.difficulty) = LOWER(?)")
                params.append(difficulty)

            if topic:
                conditions.append("LOWER(t.name) LIKE LOWER(?)")
                params.append(f"%{topic}%")

            if pattern:
                cursor.execute('SELECT pattern_id FROM Patterns WHERE LOWER(name) LIKE LOWER(?)', (f"%{pattern}%",))
                pattern_rows = cursor.fetchall()
                if not pattern_rows:
                    click.echo(f"No matching patterns found for '{pattern}'.")
                    return

                # Build OR condition for matching patterns
                pattern_ids = [row['pattern_id'] for row in pattern_rows]
                placeholders = ",".join(["?"] * len(pattern_ids))
                conditions.append(f"pp.pattern_id IN ({placeholders})")
                params.extend(pattern_ids)

            # Build query with filters
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            query += '''
                GROUP BY p.id
                ORDER BY p.priority ASC, 
                         CASE p.difficulty 
                             WHEN 'Easy' THEN 1 
                             WHEN 'Medium' THEN 2 
                             WHEN 'Hard' THEN 3 
                             ELSE 4 
                         END ASC, 
                         t.name ASC
            '''

            # Execute query
            cursor.execute(query, params)
            rows = cursor.fetchall()

            if not rows:
                click.echo("No problems found with the specified filters.")
                return

            # Implement pagination
            total_rows = len(rows)
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            paginated_rows = rows[start_idx:end_idx]

            if not paginated_rows:
                click.echo(f"No results found for page {page}.")
                return

            # Prepare output format
            table = PrettyTable()
            if compact:
                table.field_names = ["ID", "Title", "Difficulty"]
            else:
                table.field_names = ["ID", "Title", "Difficulty", "Topic", "Patterns", "URL", "Priority", "Frequency", "Prerequisites"]

            for row in paginated_rows:
                if compact:
                    table.add_row([row['id'], row['title'], row['difficulty']])
                else:
                    table.add_row([
                        row['id'], row['title'], row['difficulty'], row['topic'], 
                        row['patterns'], row['url'], row['priority'], row['frequency'], row['prerequisites']
                    ])

            # Display results
            click.echo(table)
            click.echo(f"Page {page} of {math.ceil(total_rows / per_page)}")

    except sqlite3.Error as e:
        logger.error(f"Database error in list_problems: {e}")
        click.echo("⚠️ An error occurred while listing problems.")
    except Exception as e:
        logger.error(f"Error in list_problems command: {e}")
        click.echo("⚠️ An unexpected error occurred.")


@cli.command()
@click.option('--page', type=int, default=1, help='Page number for paginated results.')
@click.option('--per-page', type=int, default=10, help='Number of results per page.')
@click.option('--filter', default=None, help='Filter patterns by name (supports partial matching).')
@click.option('--export', type=click.Choice(['csv', 'json'], case_sensitive=False), default=None, help='Export results to a file format.')
def list_patterns(page: int, per_page: int, filter: Optional[str], export: Optional[str]) -> None:
    """List all unique patterns available in the database with additional features.
    
    Usage Examples:
        list_patterns
        list_patterns --filter tree
        list_patterns --page 2 --per-page 5
        list_patterns --filter array --export csv
        list_patterns --filter string --export json
    """
    try:
        scheduler = ProblemScheduler()
        with scheduler.get_connection() as conn:
            cursor = conn.cursor()

            # Build query with optional filtering
            query = 'SELECT name FROM Patterns'
            params = []

            if filter:
                query += ' WHERE LOWER(name) LIKE LOWER(?)'
                params.append(f"%{filter}%")

            query += ' ORDER BY name ASC'

            cursor.execute(query, params)
            rows = cursor.fetchall()

            if not rows:
                click.echo("No patterns found matching the criteria.")
                return

            # Pagination
            total_rows = len(rows)
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            paginated_rows = rows[start_idx:end_idx]

            if not paginated_rows:
                click.echo(f"No results found for page {page}.")
                return

            patterns = [row['name'] for row in paginated_rows]

            # Export results if specified
            if export:
                file_name = f"patterns.{export}"
                if export == 'csv':
                    with open(file_name, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(['Pattern'])
                        writer.writerows([[pat] for pat in patterns])
                elif export == 'json':
                    with open(file_name, 'w') as jsonfile:
                        json.dump({'patterns': patterns}, jsonfile)

                click.echo(f"Patterns exported to {file_name}")
                return

            # Display results
            click.echo("Available Patterns:")
            for pat in patterns:
                click.echo(f"- {pat}")

            total_pages = math.ceil(total_rows / per_page)
            click.echo(f"Page {page} of {total_pages}")

    except sqlite3.Error as e:
        logger.error(f"Database error in list_patterns: {e}")
        click.echo("\u26a0\ufe0f An error occurred while listing patterns.")
    except Exception as e:
        logger.error(f"Error in list_patterns command: {e}")
        click.echo("\u26a0\ufe0f An unexpected error occurred.")


@cli.command()
@click.option('--limit', type=int, default=None, help='Max number of problems to solve today')
@click.option('--auto-open/--no-auto-open', default=False, help='Automatically open problem URLs in browser')
@click.option('--current-date', type=click.DateTime(formats=["%Y-%m-%d"]), default=None, help='Simulate the current date (YYYY-MM-DD)')
def today(limit: Optional[int], auto_open: bool, current_date: Optional[datetime.date]) -> None:
    """
    Show today's scheduled problems.

    Usage Examples:
        today --limit 5
        today --auto-open
        today --limit 3 --auto-open
        today --current-date 2022-12-31
        today --current-date 2022-12-31 --limit 2 --auto-open
    """
    logger.info("Started 'today' session.")
    try:
        scheduler = ProblemScheduler(current_date=current_date)
        due_problems = scheduler.get_due_problems()

        if not due_problems:
            click.echo("No problems are due today. Enjoy your break! 🎉")
            return

        # Apply limit if specified
        if limit is not None and limit < len(due_problems):
            due_problems = due_problems[:limit]

        # Sort by priority and difficulty
        due_problems.sort(key=lambda x: (
            x.priority,
            DIFFICULTY_ORDER.get(x.difficulty, 4)
        ))

        # Display sorted problems
        click.echo("Problems to solve today (in recommended order):\n")
        table = PrettyTable()
        table.field_names = ["ID", "Title", "Difficulty", "Topic", "Frequency", "Attempts", "Successes", "Time (min)", "URL"]

        for problem in due_problems:
            table.add_row([
                problem.id,
                problem.title,
                problem.difficulty,
                problem.topic,
                problem.frequency,
                problem.attempts,
                problem.successes,
                problem.time_spent,
                problem.url
            ])

        click.echo(table)

        # Initialize session summary variables
        total_time_spent = 0
        mastered_today = 0
        total_attempted = 0

        # Collect problems to solve
        problems_to_solve: List[Problem] = []
        for problem in due_problems:
            solve_choice = click.prompt(
                f"\nDo you want to solve Problem [{problem.id}]: '{problem.title}' ({problem.difficulty}, {problem.topic})?",
                type=click.Choice(['y', 'n'], case_sensitive=False),
                default='y'
            )
            if solve_choice.lower() == 'y':
                problems_to_solve.append(problem)
            else:
                click.echo(f"Skipping Problem [{problem.id}]: '{problem.title}' for now.")

        if not problems_to_solve:
            click.echo("No problems selected for solving today.")
            return

        # Solve selected problems
        for problem in problems_to_solve:
            logger.info(f"Attempting to solve Problem [{problem.id}]: '{problem.title}'")
            click.echo(f"\n--- Problem [{problem.id}]: {problem.title} ({problem.difficulty}, {problem.topic}) ---")
            click.echo(f"URL: {problem.url}")

            if auto_open:
                try:
                    webbrowser.open(problem.url)
                    click.echo("Opened problem in your default browser.")
                except webbrowser.Error as e:
                    click.echo(f"⚠️ Failed to open browser: {e} Please open the URL manually.")

            # Prompt for user input
            outcome = click.prompt("Did you solve this problem? (y/n)", type=str, default='n')
            success = (outcome.lower() == 'y')
            if success:
                logger.info(f"Problem [{problem.id}] solved successfully.")
                click.echo("Great job! ✅")
            else:
                logger.info(f"Failed to solve Problem ID {problem.id}: '{problem.title}'.")
                click.echo("Don't worry, keep practicing! 🔄")

                # Advanced inputs with validation

            hints_used_val = prompt_positive_int("Hints used?", default=0)
            time_spent_val = prompt_positive_int("Time spent (minutes)?", default=0)

            # Update progress
            try:
                scheduler.update_progress(problem.id, success, hints_used_val, time_spent_val)
            except Exception as e:
                logger.error(f"Error updating progress for Problem [{problem.id}]: {e}")
                click.echo(f"⚠️ An error occurred while updating progress for Problem [{problem.id}].")

            # Update session summary variables
            total_attempted += 1
            total_time_spent += time_spent_val
            if success:
                mastered_today += 1

        # Session Summary
        click.echo("\n--- Session Summary ---")
        click.echo(f"Problems Attempted: {total_attempted}")
        click.echo(f"Problems Mastered Today: {mastered_today}")
        click.echo(f"Total Time Spent: {total_time_spent} minutes")
        logger.info("Completed 'today' session successfully.")
    except ImportError as e:
        logger.error(f"Failed to import scheduler module: {e}")
        click.echo("⚠️ Failed to schedule today's problems due to internal error.")
    except Exception as e:
        logger.error(f"Error in today command: {e}")
        click.echo("⚠️ An unexpected error occurred during today's session.")


@cli.command(name='next-topics')
@click.option('--export', type=click.Choice(['csv', 'json'], case_sensitive=False), default=None, help='Export results to a file format (csv/json).')
@click.option('--quick', is_flag=True, default=False, help='Display quick suggestions without interactivity.')
def next_topics(export: Optional[str], quick: bool) -> None:
    """
    Suggest next topics to focus on based on mastery and prerequisites.
    
    Usage Examples:
        next-topics --export csv
        next-topics --quick
    """
    try:
        scheduler = ProblemScheduler()
        mastered_topics = set(scheduler.get_mastered_topics())

        # Determine topics that can be scheduled next
        available_topics = []
        for topic, prereqs in PREREQUISITE_MAP.items():
            if topic in mastered_topics:
                continue  # Already mastered
            # Check if all prerequisites are met
            if scheduler.can_schedule_topic(topic, mastered_topics):
                available_topics.append(topic)

        if not available_topics:
            click.echo("🎉 All topics are either mastered or prerequisites not met yet.")
            return

        # Sort available topics by priority
        available_topics.sort(key=lambda t: TopicPriority.get_priority(t, 100))

        # Prepare table data
        table_data = []
        for topic in available_topics:
            priority = TopicPriority.get_priority(topic, 100)
            prereqs = PREREQUISITE_MAP.get(topic, [])
            prereqs_str = ", ".join(prereqs) if prereqs else "None"

            # Fetch additional metrics
            try:
                metrics = scheduler.get_mastery_status(topic)
                solved_problems = metrics['solved_problems']
                success_rate = metrics['success_rate']
                success_rate = f"{success_rate * 100:.2f}%" if success_rate is not None else "N/A"
            except Exception as e:
                logger.error(f"Error fetching metrics for topic '{topic}': {e}")
                solved_problems = 0
                success_rate = "N/A"

            table_data.append([priority, topic, prereqs_str, solved_problems, success_rate])

        # Export results if specified
        if export:
            file_name = f"next_topics.{export}"
            if export == 'csv':
                with open(file_name, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Priority", "Topic", "Prerequisites", "Problems Solved", "Success Rate"])
                    writer.writerows(table_data)
            elif export == 'json':
                with open(file_name, 'w') as jsonfile:
                    json.dump({"topics": table_data}, jsonfile)

            click.echo(f"Next topics exported to {file_name}")
            return

        # Display results in quick mode or interactive mode
        if quick:
            click.echo("🔍 **Quick Suggestions for Next Topics:**")
            table = PrettyTable()
            table.field_names = ["Priority", "Topic", "Prerequisites", "Problems Solved", "Success Rate"]
            for row in table_data:
                table.add_row(row)
            click.echo(table)
            return

        # Interactive mode
        click.echo("🔍 **Next Topics to Focus On:**\n")
        table = PrettyTable()
        table.field_names = ["Priority", "Topic", "Prerequisites", "Problems Solved", "Success Rate"]
        for row in table_data:
            table.add_row(row)
        click.echo(table)

        click.echo("\n💡 **Options:**")
        click.echo("1. Explore a Topic")
        click.echo("2. Filter Suggestions")
        click.echo("3. Return to Main Menu")
        choice = click.prompt("Enter option number", type=int, default=3)

        if choice == 1:
            # List topics with numbers for selection
            click.echo("\n📚 **Select a Topic to Explore:**")
            for idx, topic in enumerate(available_topics, start=1):
                click.echo(f"{idx}. {topic}")
            topic_choice = click.prompt("Enter the number of the topic you want to explore", type=int, default=1)

            if 1 <= topic_choice <= len(available_topics):
                selected_topic = available_topics[topic_choice - 1]
                click.echo(f"\n--- **Topic:** {selected_topic} ---")
                prereqs = PREREQUISITE_MAP.get(selected_topic, [])
                prereqs_str = ", ".join(prereqs) if prereqs else "None"
                click.echo(f"**Prerequisites:** {prereqs_str}\n")

                # List related problems
                get_problems_by_topic(selected_topic)  # Use the core function
            else:
                click.echo("❌ Invalid selection. Returning to main menu.")

        elif choice == 2:
            # Implement filtering options (e.g., by difficulty)
            filter_difficulty = click.prompt("Filter by difficulty? Choose 'Easy', 'Medium', 'Hard' or 'No' to skip", type=click.Choice(['Easy', 'Medium', 'Hard', 'No'], case_sensitive=False), default='No')
            if filter_difficulty.lower() in ['easy', 'medium', 'hard']:
                filtered_topics = []
                for topic in available_topics:
                    try:
                        total, solved, success_rate = scheduler.get_additional_metrics(topic, filter_difficulty.capitalize())
                        if total > 0:
                            filtered_topics.append(topic)
                    except Exception as e:
                        logger.error(f"Error filtering topics by difficulty '{filter_difficulty}': {e}")
                        continue

                if not filtered_topics:
                    click.echo(f"No topics found with difficulty '{filter_difficulty.capitalize()}'.")
                else:
                    click.echo(f"\n🔍 **Filtered Topics (Difficulty: {filter_difficulty.capitalize()}):**\n")
                    filtered_table = PrettyTable()
                    filtered_table.field_names = ["Priority", "Topic", "Prerequisites", "Problems Solved", "Success Rate"]

                    for topic in filtered_topics:
                        priority = TopicPriority.get_priority(topic, 100)
                        prereqs = PREREQUISITE_MAP.get(topic, [])
                        prereqs_str = ", ".join(prereqs) if prereqs else "None"

                        # Fetch additional metrics
                        try:
                            metrics = scheduler.get_mastery_status(topic)
                            solved_problems = metrics['solved_problems']
                            success_rate = metrics['success_rate']
                            success_rate = f"{success_rate * 100:.2f}%" if success_rate is not None else "N/A"
                        except Exception as e:
                            logger.error(f"Error fetching metrics for topic '{topic}': {e}")
                            solved_problems = 0
                            success_rate = "N/A"

                        filtered_table.add_row([priority, topic, prereqs_str, solved_problems, success_rate])

                    click.echo(filtered_table)

                    # Option to explore filtered topics
                    explore_filtered = click.prompt("Would you like to explore a filtered topic? (y/n)", type=str, default='n')
                    if explore_filtered.lower() == 'y':
                        click.echo("\n📚 **Select a Topic to Explore:**")
                        for idx, topic in enumerate(filtered_topics, start=1):
                            click.echo(f"{idx}. {topic}")
                        filtered_topic_choice = click.prompt("Enter the number of the topic you want to explore", type=int, default=1)

                        if 1 <= filtered_topic_choice <= len(filtered_topics):
                            selected_topic = filtered_topics[filtered_topic_choice - 1]
                            click.echo(f"\n--- **Topic:** {selected_topic} ---")
                            prereqs = PREREQUISITE_MAP.get(selected_topic, [])
                            prereqs_str = ", ".join(prereqs) if prereqs else "None"
                            click.echo(f"**Prerequisites:** {prereqs_str}\n")

                            # List related problems
                            get_problems_by_topic(selected_topic)  # Use the core function
                        else:
                            click.echo("❌ Invalid selection. Returning to main menu.")
            else:
                click.echo("❌ Invalid input or skipped filtering.")

        elif choice == 3:
            click.echo("🚀 Returning to main menu.")
        else:
            click.echo("❌ Invalid option selected. Returning to main menu.")

    except ImportError as e:
        logger.error(f"Failed to import scheduler module: {e}")
        click.echo("⚠️ Failed to suggest next topics due to internal error.")
    except Exception as e:
        logger.error(f"Error in next_topics command: {e}")
        click.echo("⚠️ An unexpected error occurred while suggesting next topics.")


@cli.command(name='view-progress')  # Set the command name explicitly
@click.option('--db-path', default='leetcode_mastery.db', help='Path to the SQLite database file.')
@click.option('--output-format', default='table', type=click.Choice(['table', 'json'], case_sensitive=False),
              help='Format of the output - table or JSON.')
def view_progress(db_path: str, output_format: str) -> None:
    """
    View overall progress metrics, progress by difficulty, and progress by topic.

    Usage Examples:
        view-progress --db-path leetcode_mastery.db --output-format table
        view-progress --db-path leetcode_mastery.db --output-format json
    """
    logger.info(f"Viewing progress from database '{db_path}' with format '{output_format}'.")

    try:
        import view_progress
        view_progress.view_progress(db_path=db_path, output_format=output_format)
    except ImportError:
        logger.error("Failed to import view_progress module.")
        click.echo("⚠️ Failed to view progress due to internal error.")
    except TypeError as e:
        logger.error(f"Type error in view_progress command: {e}")
        click.echo("⚠️ An error occurred while viewing progress due to incorrect function parameters.")
    except Exception as e:
        logger.error(f"Error in view_progress command: {e}")
        click.echo("⚠️ An unexpected error occurred while viewing progress.")


@cli.command()
def visualize() -> None:
    """Generate analytics/visualizations."""
    
    try:
        import visualize_progress
        click.echo("Select Visualization:")
        click.echo("1. Success Rate Over Time")
        click.echo("2. Mastered Problems by Topic")
        click.echo("3. Success Rate by Difficulty")
        choice = click.prompt("Enter choice (1/2/3)", type=int, default=1)

        if choice == 1:
            # def plot_success_over_time(db_path: str, save_path: Optional[str] = None) -> None: -> structure of imported function
            visualize_progress.plot_success_over_time(db_path='leetcode_mastery.db')
        elif choice == 2:
            visualize_progress.plot_mastered_topics(db_path='leetcode_mastery.db')
        elif choice == 3:
            visualize_progress.plot_difficulty_success(db_path='leetcode_mastery.db')
        else:
            click.echo("Invalid choice.")
    except ImportError as e:
        logger.error(f"Failed to import visualize_progress module: {e}")
        click.echo("⚠️ Failed to generate visualization due to internal error.")
    except Exception as e:
        logger.error(f"Error in visualize command: {e}")
        click.echo("⚠️ An error occurred while generating visualization.")

if __name__ == '__main__':
    cli()
