from enum import Enum
from typing import Dict
from logger import get_logger

logger = get_logger(__name__, 'frequency_weights.log')

class FrequencyWeights(Enum):
    """
    Enum representing different frequency levels and their associated weights.
    Higher weights indicate higher frequency.
    """
    HIGH = ("High", 3)
    MEDIUM = ("Medium", 2)
    LOW = ("Low", 1)

    def __init__(self, display_name: str, weight: int):
        self.display_name = display_name
        self.weight = weight

    @classmethod
    def _display_name_to_weight_map(cls) -> Dict[str, int]:
        """
        Creates a mapping from display names (in lowercase) to their weights.

        Returns:
            Dict[str, int]: Mapping of frequency display names to weights.
        """
        return {member.display_name.lower(): member.weight for member in cls}

    @classmethod
    def get_weight(cls, frequency: str, default: int = 2) -> int:
        """
        Retrieve the weight for a given frequency display name.
        Returns a default value if the frequency is not found.

        Parameters:
            frequency (str): The display name of the frequency level.
            default (int): The default weight to return if frequency not found.

        Returns:
            int: The weight of the frequency level.
        """
        weight_map = cls._display_name_to_weight_map()
        return weight_map.get(frequency.lower(), default)

    @classmethod
    def get_weight_map(cls) -> Dict[str, int]:
        """
        Retrieve the entire weight map.

        Returns:
            Dict[str, int]: Mapping of all frequency display names to weights.
        """
        return cls._display_name_to_weight_map()

