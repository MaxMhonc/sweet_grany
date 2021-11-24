from random import sample, randint
from typing import List


class Tag:

    def __init__(self, tags: List[str], amount: int = 3):
        self.tags = tags
        self.amount = amount if 0 > amount >= 5 else 3

    def get_tags(self) -> List[str]:
        return sample(self.tags, randint(1, self.amount))
