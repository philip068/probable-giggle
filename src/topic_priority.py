from enum import Enum

class TopicPriority(Enum):
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

    def __init__(self, display_name: str, priority: int):
        self.display_name = display_name
        self.priority = priority

    @classmethod
    def get_priority(cls, topic: str, default: int = 100) -> int:
        """
        Retrieve the priority for a given topic display name.
        Returns a default value if the topic is not found.
        """
        for member in cls:
            if member.display_name.lower() == topic.lower():
                return member.priority
        return default
