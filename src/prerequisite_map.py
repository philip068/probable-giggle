from typing import List, Dict
from topic_priority import TopicPriority
from logger import get_logger

logger = get_logger(__name__, 'prerequisite_map.log')

PREREQUISITE_MAP: Dict[str, List[str]] = {
    "Array": [],
    "String": [],
    "Linked List": ["Array"],
    "Hash Table": ["Array"],
    "Stack": ["Array"],
    "Queue": ["Array"],
    "Tree": ["Array", "Linked List"],
    "Binary Tree": ["Tree"],
    "Binary Search Tree": ["Binary Tree"],
    "Graph": ["Tree"],
    "Heap": ["Array"],
    "Dynamic Programming": ["Recursion", "Array", "Math"],
    "Greedy": ["Sorting", "Array"],
    "Backtracking": ["Recursion", "Tree"],
    "Bit Manipulation": ["Math"],
    "Trie": ["String"],
    "Union-Find": ["Hash Table"],
    "Segment Tree": ["Binary Tree"],
    "Topological Sort": ["Graph"],
    "Binary Search": ["Array"],
    "Sorting": ["Array"],
    "Math": [],
    "Database": ["Array", "String", "Linked List", "Hash Table",]
}

def validate_prerequisite_map() -> None:
    """
    Validates that all topics and their prerequisites exist in the TopicPriority enum.
    Raises exceptions for any inconsistencies.
    """
    valid_topics = {member.display_name for member in TopicPriority}
    for topic, prereqs in PREREQUISITE_MAP.items():
        if topic not in valid_topics:
            logger.error(f"Topic '{topic}' is not defined in TopicPriority enum.")
            raise ValueError(f"Undefined topic '{topic}' in PREREQUISITE_MAP.")
        for prereq in prereqs:
            if prereq not in valid_topics:
                logger.error(f"Prerequisite topic '{prereq}' for topic '{topic}' is not defined in TopicPriority enum.")
                raise ValueError(f"Undefined prerequisite topic '{prereq}' for topic '{topic}' in PREREQUISITE_MAP.")

# Perform validation at import time
validate_prerequisite_map()
