from typing import List, Dict

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
}
