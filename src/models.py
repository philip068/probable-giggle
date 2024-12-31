from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Problem:
    id: int
    title: str
    difficulty: str
    topic: str
    patterns: List[str]
    frequency: str
    url: str
    priority: int
    prerequisites: List[int]
    attempts: int = 0
    successes: int = 0
    hints_used: int = 0
    time_spent: int = 0
    last_attempt: Optional[str] = None
    next_due: Optional[str] = None
    mastered: bool = False
