import sqlite3
import datetime
import sys
from typing import Generator, List, Set, Optional, Tuple, Dict
from contextlib import contextmanager
from dataclasses import dataclass
from functools import lru_cache
import configparser

# Import configurations
from topic_priority import TopicPriority
from frequency_weights import FrequencyWeights
from pattern_weights import PatternWeights
from prerequisite_map import PREREQUISITE_MAP, validate_prerequisite_map
from models import Problem
from logger import get_logger

logger = get_logger(__name__, 'scheduler.log')

class ProblemScheduler:
    """
    Handles problem scheduling, fetching due problems, calculating scores, and updating user progress.
    """
    # Class-level constants
    DIFFICULTY_ORDER: Dict[str, int] = {"Easy": 1, "Medium": 2, "Hard": 3}

    def __init__(self, current_date: Optional[datetime.date] = None):
        """
        Initialize the ProblemScheduler with the specified database path.
        
        Parameters:
            db_path (str): Path to the SQLite database file.
        """

        self.current_date = current_date or datetime.date.today()
        validate_prerequisite_map() 

        config = configparser.ConfigParser()
        config_path = 'config.ini'
        read_files = config.read(config_path)
        config.read('config.ini')

        config = configparser.ConfigParser()
        config_path = 'config.ini'  # Ensure this path is correct
        read_files = config.read(config_path)

        if not read_files:
            logger.error(f"Configuration file '{config_path}' not found.")
            print(f"⚠️ Configuration error: '{config_path}' not found.")
            sys.exit(1)

        required_sections = ['Database', 'Scheduling', 'Scoring']
        for section in required_sections:
            if section not in config:
                logger.error(f"Missing section '{section}' in config.ini.")
                print(f"⚠️ Configuration error: Missing section '{section}' in config.ini.")
                sys.exit(1)

        required_keys = {
            'Database': ['db_path'],
            'Scheduling': ['spaced_intervals', 'mastery_threshold_ratio', 'min_attempts_for_mastery'],
            'Scoring': [
                'difficulty_weight_multiplier', 'default_topic_priority', 'default_difficulty_weight',
                'default_pattern_weight', 'pattern_weight_multiplier', 'default_frequency_weight',
                'frequency_weight_multiplier', 'base_urgency_score', 'time_normalization_factor',
                'attempt_penalty', 'invert_topic_priority_base', 'hints_factor', 'topic_priority_offset'
            ]
        }

        for section, keys in required_keys.items():
            for key in keys:
                if key not in config[section]:
                    logger.error(f"Missing key '{key}' in section '{section}' of config.ini.")
                    print(f"⚠️ Configuration error: Missing key '{key}' in section '{section}' of config.ini.")
                    sys.exit(1)
            
        self.db_path = config['Database']['db_path']
        self.SPACED_INTERVALS = list(map(int, config['Scheduling']['spaced_intervals'].split(',')))
        self.MASTERY_THRESHOLD_RATIO = float(config['Scheduling']['mastery_threshold_ratio'])
        self.MIN_ATTEMPTS_FOR_MASTERY = int(config['Scheduling']['min_attempts_for_mastery'])
        self.DEFAULT_DIFFICULTY_WEIGHT = int(config['Scoring']['default_difficulty_weight'])
        self.DEFAULT_TOPIC_PRIORITY = int(config['Scoring']['default_topic_priority'])
        self.DEFAULT_FREQ_WEIGHT = int(config['Scoring']['default_frequency_weight'])
        self.DEFAULT_PATTERN_WEIGHT = int(config['Scoring']['default_pattern_weight'])
        self.BASE_URGENCY_FACTOR = float(config['Scoring']['base_urgency_score'])
        self.TIME_NORMALIZATION_FACTOR = float(config['Scoring']['time_normalization_factor'])
        self.ATTEMPT_PENALTY = float(config['Scoring']['attempt_penalty'])
        self.INVERT_TOPIC_PRIORITY_BASE = int(config['Scoring']['invert_topic_priority_base'])
        self.HINTS_FACTOR = float(config['Scoring']['hints_factor'])
        self.PATTERN_WEIGHT_MULTIPLIER = float(config['Scoring']['pattern_weight_multiplier'])
        self.FREQUENCY_WEIGHT_MULTIPLIER = float(config['Scoring']['frequency_weight_multiplier'])
        self.DIFFICULTY_WEIGHT_MULTIPLIER = float(config['Scoring']['difficulty_weight_multiplier'])
        self.TOPIC_PRIORITY_OFFSET = int(config['Scoring']['topic_priority_offset'])


    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """
        Context manager for SQLite database connection.
        
        Yields:
            sqlite3.Connection: SQLite connection object.
        """
        conn: Optional[sqlite3.Connection] = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    @lru_cache(maxsize=128)
    def get_mastered_topics(self) -> Set[str]:
        """
        Determine which topics have been mastered based on problem mastery.
        A topic is considered mastered if at least MASTERY_THRESHOLD_RATIO of its problems are mastered.
        
        Returns:
            Set[str]: Set of mastered topic names.
        """
        mastered_topics: Set[str] = set()
        query: str = '''
            SELECT t.name AS topic, COUNT(p.id) AS total, 
                   SUM(CASE WHEN up.mastered = 1 THEN 1 ELSE 0 END) AS mastered_count
            FROM Problems p
            JOIN Topics t ON p.topic_id = t.topic_id
            LEFT JOIN UserProgress up ON p.id = up.problem_id
            GROUP BY t.name
        '''
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
            except sqlite3.Error as e:
                logger.error(f"Error fetching mastered topics: {e}")
                return mastered_topics

        for row in rows:
            topic: str = row['topic']
            total: int = row['total']
            mastered_count: int = row['mastered_count'] or 0
            mastery_ratio: float = mastered_count / total if total > 0 else 0

            if mastery_ratio >= self.MASTERY_THRESHOLD_RATIO:
                mastered_topics.add(topic)
                logger.debug(f"Topic '{topic}' mastered with ratio {mastery_ratio:.2f}")

        logger.info(f"Mastered topics: {mastered_topics}")
        return mastered_topics

    def can_schedule_topic(self, topic: str, mastered_topics: Set[str]) -> bool:
        """
        Check if all prerequisites for a topic are mastered.
        
        Parameters:
            topic (str): The topic to check.
            mastered_topics (Set[str]): Set of already mastered topics.
        
        Returns:
            bool: True if the topic can be scheduled, False otherwise.
        """
        prerequisites: List[str] = PREREQUISITE_MAP.get(topic, [])
        missing: List[str] = [prereq for prereq in prerequisites if prereq not in mastered_topics]
        if missing:
            logger.debug(f"Cannot schedule topic '{topic}' as prerequisites {missing} are not mastered.")
            return False
        logger.debug(f"All prerequisites for topic '{topic}' are mastered.")
        return True

    def check_prereq_mastery(self, prereq_ids: List[int]) -> bool:
        """
        Return True if all prerequisite problems are mastered, else False.
        
        Parameters:
            prereq_ids (List[int]): List of prerequisite problem IDs.
        
        Returns:
            bool: True if all prerequisites are mastered, False otherwise.
        """
        if not prereq_ids:
            return True

        placeholders: str = ','.join(['?'] * len(prereq_ids))
        query: str = f'''
            SELECT COUNT(*) AS mastered_count
            FROM UserProgress
            WHERE problem_id IN ({placeholders}) AND mastered = 1
        '''
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, prereq_ids)
                mastered_count: int = cursor.fetchone()['mastered_count']
            except sqlite3.Error as e:
                logger.error(f"Error checking prerequisite mastery: {e}")
                return False

        all_mastered: bool = mastered_count == len(prereq_ids)
        logger.debug(f"Prerequisite mastery check: {all_mastered} (Mastered {mastered_count}/{len(prereq_ids)})")
        return all_mastered

    @lru_cache(maxsize=None)
    def get_topic_priority_map(self) -> Dict[str, int]:
        """
        Retrieve a mapping of topics to their priorities.

        Returns:
            Dict[str, int]: Mapping of topic names to priorities.
        """
        return TopicPriority.get_priority_map()
    
    @lru_cache(maxsize=None)
    def get_frequency_weight_map(self) -> Dict[str, int]:
        """
        Retrieve a mapping of frequency levels to their weights.

        Returns:
            Dict[str, int]: Mapping of frequency levels to weights.
        """
        return FrequencyWeights.get_weight_map()
    
    @lru_cache(maxsize=None)
    def get_pattern_weight_map(self) -> Dict[str, int]:
        """
        Retrieve a mapping of patterns to their weights.

        Returns:
            Dict[str, int]: Mapping of pattern names to weights.
        """
        return PatternWeights.get_weight_map()

    def calculate_problem_score(
        self,
        problem: Problem
    ) -> float:
        """
        Compute a final score for the given problem based on various factors.
        Higher score indicates higher urgency.
        
        Parameters:
            problem (Problem): The problem instance.
        
        Returns:
            float: Calculated score representing urgency.
        """
        # 1) Base difficulty weighting (lower for easier problems)
        diff_weight: int = self.DIFFICULTY_ORDER.get(problem.difficulty, self.DEFAULT_DIFFICULTY_WEIGHT)

        # 2) Topic Priority (higher priority topics have higher scores)
        topic_priority: int = self.get_topic_priority_map().get(problem.topic, self.DEFAULT_TOPIC_PRIORITY)

        # 3) Frequency weighting (Higher frequency means higher urgency)
        freq_weight: int = self.get_frequency_weight_map().get(problem.frequency.lower(), self.DEFAULT_FREQ_WEIGHT)

        # 4) Patterns weighting
        pattern_score: float = sum(
            self.get_pattern_weight_map().get(pat.lower(), self.DEFAULT_PATTERN_WEIGHT) 
            for pat in problem.patterns
        )
        # Log unknown patterns
        for pat in problem.patterns:
            if pat.lower() not in self.get_pattern_weight_map():
                logger.warning(f"Unknown pattern '{pat}' encountered. Using default weight.")

        # 5) Performance-based factor
        if problem.attempts == 0:
            urgency_factor = self.BASE_URGENCY_FACTOR * 1.0  # Assign maximum urgency
        else:
            success_rate = problem.successes / problem.attempts
            urgency_factor = self.BASE_URGENCY_FACTOR * (1 - success_rate)

        # 6) Hints and time spent increase urgency
        hints_factor: float = problem.hints_used * self.HINTS_FACTOR
        time_factor: float = problem.time_spent / self.TIME_NORMALIZATION_FACTOR  # Normalize time spent

        # 7) Attempts slightly decrease urgency (more attempts might mean less urgent)
        attempts_factor: float = -self.ATTEMPT_PENALTY * problem.attempts

        # Final score calculation
        score: float = (
            (diff_weight * self.DIFFICULTY_WEIGHT_MULTIPLIER) +                      # Weighted difficulty
            (self.INVERT_TOPIC_PRIORITY_BASE - topic_priority) +  # Inverted topic priority
            (pattern_score * self.PATTERN_WEIGHT_MULTIPLIER) +                   # Weighted patterns
            (freq_weight * self.FREQUENCY_WEIGHT_MULTIPLIER) +                       # Weighted frequency
            urgency_factor +                          # Performance-based urgency
            hints_factor +                            # Hints used
            time_factor +                             # Time spent
            attempts_factor                           # Attempts
        )

        logger.debug(f"Calculated score {score:.2f} for problem '{problem.title}' (ID={problem.id})")
        return score

    def get_due_problems(self) -> List[Problem]:
        """
        Retrieve due problems considering priority, dependencies, and spaced repetition.
        Returns a list of Problem instances sorted by their calculated scores.
        
        Returns:
            List[Problem]: Sorted list of due problems.
        """
        today: str = self.current_date.isoformat()
        query: str = '''
            SELECT p.id, p.title, p.difficulty, t.name AS topic, p.frequency,
                p.url, p.priority, up.attempts, up.successes, up.hints_used, 
                up.time_spent, up.last_attempt, up.next_due, up.mastered, up.current_interval_index
            FROM Problems p
            JOIN Topics t ON p.topic_id = t.topic_id
            LEFT JOIN UserProgress up ON p.id = up.problem_id
            WHERE (DATE(up.next_due) <= DATE(?) OR up.next_due IS NULL)
        '''


        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (today,))
                all_due: sqlite3.Row = cursor.fetchall()
            except sqlite3.Error as e:
                logger.error(f"Error fetching due problems: {e}")
                return []

        mastered_topics: Set[str] = self.get_mastered_topics()
        sorted_problems_with_scores: List[Tuple[float, Problem]] = []

        # Fetch all patterns and prerequisites in bulk to optimize performance
        patterns_map: Dict[int, List[str]] = self.fetch_all_patterns()
        prereqs_map: Dict[int, List[int]] = self.fetch_all_prerequisites()

        for row in all_due:
            problem: Problem = self.row_to_problem(row, patterns_map, prereqs_map)

            if not self.can_schedule_topic(problem.topic, mastered_topics):
                continue

            if problem.prerequisites:
                prereq_ids: List[int] = problem.prerequisites
                if not self.check_prereq_mastery(prereq_ids):
                    continue

            score: float = self.calculate_problem_score(problem)
            sorted_problems_with_scores.append((score, problem))

        # Sort problems by descending score (higher score = more urgent)
        sorted_problems_with_scores.sort(key=lambda x: x[0], reverse=True)

        # Extract sorted Problem instances
        sorted_problems: List[Problem] = [item[1] for item in sorted_problems_with_scores]

        logger.info(f"Retrieved {len(sorted_problems)} due problems.")
        return sorted_problems

    def update_progress(
        self,
        problem_id: int,
        success: bool,
        hints_used: int = 0,
        time_spent: int = 0
    ) -> None:
        """
        Update user progress after attempting a problem.
        
        Parameters:
            problem_id (int): ID of the problem.
            success (bool): Whether the problem was solved successfully.
            hints_used (int): Number of hints used.
            time_spent (int): Time spent solving the problem in minutes.
        """
        today: str = self.current_date.isoformat()
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('BEGIN')

                # Fetch existing progress
                cursor.execute('''
                    SELECT attempts, successes, hints_used, time_spent, current_interval_index, mastered
                    FROM UserProgress
                    WHERE problem_id = ?
                ''', (problem_id,))
                row: Optional[sqlite3.Row] = cursor.fetchone()

                 # Initialize or update progress stats
                attempts = row['attempts'] + 1 if row else 1
                successes = row['successes'] + int(success) if row else int(success)
                total_hints = row['hints_used'] + hints_used if row else hints_used
                total_time = row['time_spent'] + time_spent if row else time_spent
                mastered = row['mastered'] if row else False
                current_interval_index = row['current_interval_index'] if row else -1  # Start before first interval

                # Determine next interval and due date
                next_interval_index, next_due, is_still_mastered = self.get_next_progress(current_interval_index, success, attempts, successes, mastered)

                if row:
                    cursor.execute('''
                        UPDATE UserProgress
                        SET attempts = ?, successes = ?, hints_used = ?, time_spent = ?,
                            last_attempt = ?, next_due = ?, mastered = ?, current_interval_index = ?
                        WHERE problem_id = ?
                    ''', (attempts, successes, total_hints, total_time,
                        today, next_due, is_still_mastered, next_interval_index, problem_id))
                else:
                    cursor.execute('''
                    INSERT INTO UserProgress (
                        problem_id, attempts, successes, hints_used, time_spent,
                        last_attempt, next_due, mastered, current_interval_index
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (problem_id, attempts, successes, total_hints, total_time,
                      today, next_due, is_still_mastered, next_interval_index))

                conn.commit()
                logger.info(f"Updated progress for problem ID {problem_id}. Mastered: {mastered}")
        except sqlite3.Error as e:
            logger.error(f"Error updating progress for problem ID {problem_id}: {e}")
            raise


    def get_next_progress(self, current_interval_index: int, success: bool, attempts: int, successes: int, mastered: bool) -> Tuple[int, str]:
        """
        Determine the next interval index and due date based on progress.

        Parameters:
            current_interval_index (int): Current interval index in SPACED_INTERVALS.
            success (bool): Whether the current attempt was successful.
            attempts (int): Total attempts so far.
            successes (int): Total successes so far.

        Returns:
            Tuple[int, str]: Next interval index and due date as ISO string.
        """
        is_still_mastered = self.check_mastery(attempts, successes, mastered)

        if success:
            next_interval_index = min(current_interval_index + 1, len(self.SPACED_INTERVALS) - 1)
        elif is_still_mastered:
            next_interval_index = max(current_interval_index - 1, 0)
        else:
            next_interval_index = 0

        next_due = self.calculate_next_due(next_interval_index, success)
        return next_interval_index, next_due, is_still_mastered
        

    def check_mastery(self, attempts: int, successes: int, mastered: bool) -> bool:
        """
        Determine if a problem is mastered based on success rate, attempts, and the current mastery status.
        
        Parameters:
            attempts (int): Number of attempts made.
            successes (int): Number of successful attempts.
            mastered (bool): Current mastery status.
        
        Returns:
            bool: True if mastered, False otherwise.
        """
        if mastered:
            logger.debug(f"Problem already mastered.")
            return True
        if attempts >= self.MIN_ATTEMPTS_FOR_MASTERY and (successes / attempts) >= self.MASTERY_THRESHOLD_RATIO:
            logger.debug(f"Problem mastered: {successes}/{attempts} successes.")
            return True
        logger.debug(f"Problem not mastered: {successes}/{attempts} successes.")
        return False

    def calculate_next_due(self, interval_index: int, success: bool) -> str:
        """
        Calculate the next due date based on success status and interval index.

        Parameters:
            interval_index (int): The index in SPACED_INTERVALS for the interval to use.
            success (bool): Whether the attempt was successful (default is True).

        Returns:
            str: ISO-formatted date string for the next due date.
        """
        today = self.current_date
        days_to_next_due = self.SPACED_INTERVALS[interval_index] if success else 1
        next_due = today + datetime.timedelta(days=days_to_next_due)
        logger.debug(f"Next due date calculated as {next_due.isoformat()} for {'success' if success else 'failure'} attempt.")
        return next_due.isoformat()



    def get_additional_metrics(self, topic: str, difficulty: Optional[str] = None) -> Tuple[int, int, Optional[float]]:
        """
        Retrieve additional metrics for a topic.
        Returns total problems, solved problems, and average success rate.
        
        Parameters:
            topic (str): The topic name.
            difficulty (Optional[str]): Difficulty level to filter.
        
        Returns:
            Tuple[int, int, Optional[float]]: Total problems, solved problems, success rate.
        """
        total_query: str = '''
            SELECT COUNT(*) AS total
            FROM Problems p
            JOIN UserProgress up ON p.id = up.problem_id
            WHERE p.topic_id = (SELECT topic_id FROM Topics WHERE name = ?) {difficulty_filter}
        '''
        solved_query: str = '''
            SELECT COUNT(*) AS solved
            FROM UserProgress up
            JOIN Problems p ON up.problem_id = p.id
            WHERE p.topic_id = (SELECT topic_id FROM Topics WHERE name = ?) {difficulty_filter} AND up.successes > 0
        '''
        success_rate_query: str = '''
            SELECT AVG(CAST(up.successes AS FLOAT)/CAST(up.attempts AS FLOAT)) AS success_rate
            FROM UserProgress up
            JOIN Problems p ON up.problem_id = p.id
            WHERE p.topic_id = (SELECT topic_id FROM Topics WHERE name = ?) {difficulty_filter} AND up.attempts > 0
        '''

        difficulty_filter: str = f"AND p.difficulty = '{difficulty.capitalize()}'" if difficulty else ""
        params: Tuple[str, ...] = (topic,)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(total_query.format(difficulty_filter=difficulty_filter), params)
                total: int = cursor.fetchone()['total'] or 0

                cursor.execute(solved_query.format(difficulty_filter=difficulty_filter), params)
                solved: int = cursor.fetchone()['solved'] or 0

                cursor.execute(success_rate_query.format(difficulty_filter=difficulty_filter), params)
                success_rate: Optional[float] = cursor.fetchone()['success_rate']
            except sqlite3.Error as e:
                logger.error(f"Error retrieving additional metrics for topic '{topic}': {e}")
                return (0, 0, None)

        return (total, solved, success_rate)

    def get_mastery_status(self, topic: str) -> dict:
        """
        Get mastery status metrics for a topic.
        Returns a dictionary with total problems, solved problems, and success rate.
        
        Parameters:
            topic (str): The topic name.
        
        Returns:
            dict: Mastery status metrics.
        """
        total_problems, solved_problems, success_rate = self.get_additional_metrics(topic)
        return {
            'total_problems': total_problems,
            'solved_problems': solved_problems,
            'success_rate': success_rate
        }

    def row_to_problem(
        self,
        row: sqlite3.Row,
        patterns_map: Dict[int, List[str]],
        prereqs_map: Dict[int, List[int]]
    ) -> Problem:
        """
        Convert a database row to a Problem instance using pre-fetched patterns and prerequisites.
        
        Parameters:
            row (sqlite3.Row): Database row representing a problem.
            patterns_map (Dict[int, List[str]]): Mapping of problem_id to patterns.
            prereqs_map (Dict[int, List[int]]): Mapping of problem_id to prerequisite IDs.
        
        Returns:
            Problem: The Problem instance.
        """
        problem = Problem(
            id=row['id'],
            title=row['title'],
            difficulty=row['difficulty'],
            topic=row['topic'],
            patterns=patterns_map.get(row['id'], []),
            frequency=row['frequency'],
            url=row['url'],
            priority=row['priority'],
            prerequisites=prereqs_map.get(row['id'], []),
            attempts=row['attempts'] or 0,
            successes=row['successes'] or 0,
            hints_used=row['hints_used'] or 0,
            time_spent=row['time_spent'] or 0,
            last_attempt=row['last_attempt'],
            next_due=row['next_due'],
            mastered=bool(row['mastered']) if row['mastered'] is not None else False
        )
        return problem

    def fetch_all_patterns(self) -> Dict[int, List[str]]:
        """
        Fetch all patterns associated with each problem in bulk.
        
        Returns:
            Dict[int, List[str]]: Mapping of problem_id to list of pattern names.
        """
        query: str = '''
            SELECT pp.problem_id, pr.name
            FROM ProblemPatterns pp
            JOIN Patterns pr ON pp.pattern_id = pr.pattern_id
        '''
        patterns_map: Dict[int, List[str]] = {}
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                rows: List[sqlite3.Row] = cursor.fetchall()
                for row in rows:
                    problem_id: int = row['problem_id']
                    pattern_name: str = row['name']
                    patterns_map.setdefault(problem_id, []).append(pattern_name)
            except sqlite3.Error as e:
                logger.error(f"Error fetching all patterns: {e}")
        logger.debug(f"Fetched patterns for {len(patterns_map)} problems.")
        return patterns_map

    def fetch_all_prerequisites(self) -> Dict[int, List[int]]:
        """
        Fetch all prerequisites associated with each problem in bulk.
        
        Returns:
            Dict[int, List[int]]: Mapping of problem_id to list of prerequisite IDs.
        """
        query: str = '''
            SELECT problem_id, prerequisite_id
            FROM ProblemPrerequisites
        '''
        prereqs_map: Dict[int, List[int]] = {}
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                rows: List[sqlite3.Row] = cursor.fetchall()
                for row in rows:
                    problem_id: int = row['problem_id']
                    prereq_id: int = row['prerequisite_id']
                    prereqs_map.setdefault(problem_id, []).append(prereq_id)
            except sqlite3.Error as e:
                logger.error(f"Error fetching all prerequisites: {e}")
        logger.debug(f"Fetched prerequisites for {len(prereqs_map)} problems.")
        return prereqs_map