from random import shuffle
from copy import copy
from typing import List


class Author:
    """
    Author's instance picks up names from self.full_names without repeating
    until names will not run out.
    Then it begin to repeat names.
    """

    def __init__(self, full_names: list):
        self.full_names = full_names
        self._shuffled_names = None
        self._set_shuffled_names()

    def get_random_name(self) -> str:
        name = self._shuffled_names.pop()
        if not self._shuffled_names:
            self._set_shuffled_names()
        return name

    def _shuffle_names(self) -> List[str]:
        names_to_shuffle = copy(self.full_names)
        shuffle(names_to_shuffle)
        return names_to_shuffle

    def _set_shuffled_names(self):
        self._shuffled_names = self._shuffle_names()
