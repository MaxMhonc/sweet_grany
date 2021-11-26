from random import choice
from typing import List


class Author:
    """
    Author instance is initialised with full_names list and via
    get_random_name_generator returns them one by one in random order until it
    is run out.
    """

    def __init__(self, full_names: List[str]):
        self.full_names = full_names

    def get_all_authors(self) -> List[str]:
        """Returns all available authors"""
        return self.full_names

    def get_random_author(self) -> int:
        """Returns random name from 'full_names'"""
        return choice(self.full_names)
