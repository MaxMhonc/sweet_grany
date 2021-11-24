from random import shuffle
from typing import List


class Author:
    """
    Author instance is initialised with full_names list and via
    get_random_name_generator returns them one by one in random order until it
    is run out.
    """

    def __init__(self, full_names: List[str]):
        self.full_names = full_names
        self._shuffle_names()

    def get_random_name_generator(self) -> str:
        yield from (name for name in self.full_names)

    def _shuffle_names(self):
        shuffle(self.full_names)

