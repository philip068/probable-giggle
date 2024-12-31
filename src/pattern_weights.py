from enum import Enum
from typing import Dict
from logger import get_logger

logger = get_logger(__name__, 'pattern_weights.log')
class PatternWeights(Enum):
    """
    Enum representing different problem-solving patterns and their associated weights.
    Higher weights indicate higher importance or urgency.
    """
    TWO_POINTERS = ("Two Pointers", 5)
    SLIDING_WINDOW = ("Sliding Window", 5)
    RECURSION = ("Recursion", 4)
    ITERATION = ("Iteration", 4)
    DIVIDE_AND_CONQUER = ("Divide and Conquer", 3)
    MATH = ("Math", 6)
    GREEDY = ("Greedy", 3)
    BACKTRACKING = ("Backtracking", 2)
    DFS = ("Depth-First Search", 3)
    BFS = ("Breadth-First Search", 3)
    DESIGN = ("Design", 3)
    DYNAMIC_PROGRAMMING = ("Dynamic Programming", 3)
    BIT_MANIPULATION = ("Bit Manipulation", 2)
    TOP_DOWN_DP = ("Top-Down DP", 3)
    BOTTOM_UP_DP = ("Bottom-Up DP", 3)
    MEMOIZATION = ("Memoization", 3)
    TABULATION = ("Tabulation", 3)
    KWAY_PARTITIONING = ("K-Way Partitioning", 1)
    RANDOMIZATION = ("Randomization", 1)
    BRANCH_AND_BOUND = ("Branch and Bound", 1)
    PARALLEL_ALGORITHMS = ("Parallel Algorithms", 1)
    TRIE = ("Trie", 2)
    UNION_FIND = ("Union-Find", 3)
    HASH_TABLE = ("Hash Table", 4)
    STACK = ("Stack", 4)

    def __init__(self, display_name: str, weight: int):
        self.display_name = display_name
        self.weight = weight

    @classmethod
    def _display_name_to_weight_map(cls) -> Dict[str, int]:
        """
        Creates a mapping from display names (in lowercase) to their weights.

        Returns:
            Dict[str, int]: Mapping of pattern display names to weights.
        """
        return {member.display_name.lower(): member.weight for member in cls}

    @classmethod
    def get_weight(cls, pattern: str, default: int = 1) -> int:
        """
        Retrieve the weight for a given pattern display name.
        Returns a default value if the pattern is not found.

        Parameters:
            pattern (str): The display name of the pattern.
            default (int): The default weight to return if pattern not found.

        Returns:
            int: The weight of the pattern.
        """
        weight_map = cls._display_name_to_weight_map()
        return weight_map.get(pattern.lower(), default)

    @classmethod
    def get_weight_map(cls) -> Dict[str, int]:
        """
        Retrieve the entire weight map.

        Returns:
            Dict[str, int]: Mapping of all pattern display names to weights.
        """
        return cls._display_name_to_weight_map()

