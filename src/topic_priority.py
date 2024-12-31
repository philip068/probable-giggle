from enum import Enum
from typing import Dict
from logger import get_logger

logger = get_logger(__name__, 'topic_priority.log')

class TopicPriority(Enum):
    """
    Enum representing different topics and their associated priorities.
    Lower numerical values indicate higher priority.
    """
    ARRAY = ("Array", 1)
    STRING = ("String", 2)
    LINKED_LIST = ("Linked List", 3)
    HASH_TABLE = ("Hash Table", 4)
    STACK = ("Stack", 5)
    QUEUE = ("Queue", 6)
    TREE = ("Tree", 7)
    BINARY_TREE = ("Binary Tree", 8)
    BINARY_SEARCH_TREE = ("Binary Search Tree", 9)
    GRAPH = ("Graph", 10)
    HEAP = ("Heap", 11)
    DYNAMIC_PROGRAMMING = ("Dynamic Programming", 12)
    GREEDY = ("Greedy", 13)
    BACKTRACKING = ("Backtracking", 14)
    BIT_MANIPULATION = ("Bit Manipulation", 15)
    TRIE = ("Trie", 16)
    UNION_FIND = ("Union-Find", 17)
    SEGMENT_TREE = ("Segment Tree", 18)
    TOPOLOGICAL_SORT = ("Topological Sort", 19)
    BINARY_SEARCH = ("Binary Search", 20)
    SORTING = ("Sorting", 21)
    MATH = ("Math", 22)
    RECURSION = ("Recursion", 23)
    DATABASE = ("Database", 24)

    def __init__(self, display_name: str, priority: int):
        self.display_name = display_name
        self.priority = priority

    @classmethod
    def _display_name_to_priority_map(cls) -> Dict[str, int]:
        """
        Creates a mapping from display names (in lowercase) to their priorities.

        Returns:
            Dict[str, int]: Mapping of topic display names to priorities.
        """
        return {member.display_name.lower(): member.priority for member in cls}

    @classmethod
    def get_priority(cls, topic: str, default: int = 100) -> int:
        """
        Retrieve the priority for a given topic display name.
        Returns a default value if the topic is not found.

        Parameters:
            topic (str): The display name of the topic.
            default (int): The default priority to return if topic not found.

        Returns:
            int: The priority of the topic.
        """
        priority_map = cls._display_name_to_priority_map()
        return priority_map.get(topic.lower(), default)

    @classmethod
    def get_priority_map(cls) -> Dict[str, int]:
        """
        Retrieve the entire priority map.

        Returns:
            Dict[str, int]: Mapping of all topic display names to priorities.
        """
        return cls._display_name_to_priority_map()

