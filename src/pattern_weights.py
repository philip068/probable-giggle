from enum import Enum

class PatternWeights(Enum):
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
    DYNAMIC_PROGRAMMING = ("Dynamic Programming", 5)
    BIT_MANIPULATION = ("Bit Manipulation", 2)
    TOP_DOWN_DP = ("Top-Down DP", 4)
    BOTTOM_UP_DP = ("Bottom-Up DP", 4)
    MEMOIZATION = ("Memoization", 4)
    TABULATION = ("Tabulation", 4)
    KWAY_PARTITIONING = ("K-Way Partitioning", 1)
    RANDOMIZATION = ("Randomization", 1)
    BRANCH_AND_BOUND = ("Branch and Bound", 1)
    PARALLEL_ALGORITHMS = ("Parallel Algorithms", 1)

    def __init__(self, display_name: str, weight: int):
        self.display_name = display_name
        self.weight = weight

    @classmethod
    def get_weight(cls, pattern: str, default: int = 1) -> int:
        """
        Retrieve the weight for a given pattern display name.
        Returns a default value if the pattern is not found.
        """
        for member in cls:
            if member.display_name.lower() == pattern.lower():
                return member.weight
        return default
