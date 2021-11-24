from random import choice
from typing import Tuple, List, Optional
from itertools import zip_longest


class Recipe:
    """
    Recipe instance generates little crazy recipes for self.prods.
    All recipes consist from "clean step", "prepare step", "merge step",
    "cook step" and "finalize step". Actions for every step are set via
    verbs lists in corresponded variables.
    """

    def __init__(
            self,
            clean_verbs: List[str],
            prepare_verbs: List[str],
            merge_verbs: List[str],
            cook_verbs: List[str],
            finalize_verbs: List[str],
            products: List[str]
    ):
        self.clean_verbs = clean_verbs
        self.prepare_verbs = prepare_verbs
        self.merge_verbs = merge_verbs
        self.cook_verbs = cook_verbs
        self.finalize_verbs = finalize_verbs
        self.prods = products
        self.final_prod = None

    def get_text(self) -> str:
        """Build and return whale recipe."""
        steps = []

        cleaning = [(self._generate_clean_step(prod), prod)
                    for prod in self.prods]
        steps.append(f"Step 1.\n{self._list_to_str(cleaning)}")
        self.prods = [item[1] for item in cleaning]

        preparing = [(self._generate_prepare_step(prod), prod)
                     for prod in self.prods]
        steps.append(f"Step 2.\n{self._list_to_str(preparing)}.")
        self.prods, self.final_prod = self._pair_up([item[1]
                                                     for item in cleaning])

        merge = [(self._generate_merge_step(pair),
                  f"mix of {pair[0]} and {pair[1]}") for pair in self.prods]
        steps.append(f"Step 3.\n{self._list_to_str(merge)}.")
        self.prods = [item[1] for item in merge]

        cook = [self._generate_cook_step(prod) for prod in self.prods]
        steps.append(f"Step 4.\n{self._list_to_str(cook)}.")
        self.prods = [item[1] for item in cook]

        if self.final_prod:
            steps.append(f'Step 5.\nDecorate dish with {self.final_prod}')

        return '\n'.join(steps)

    def _generate_clean_step(self, prod: str) -> str:
        return f'{self._get_action(self.clean_verbs)} the {prod}'

    def _generate_prepare_step(self, prod: str) -> str:
        return f'{self._get_action(self.prepare_verbs)} the {prod}'

    def _generate_merge_step(self, prods_pair: Tuple[str, str]) -> str:
        return f'{self._get_action(self.merge_verbs)} the {prods_pair[0]}' \
               f' with {prods_pair[1]}'

    def _generate_cook_step(self, prod: str) -> Tuple[str, str]:
        action = self._get_action(self.cook_verbs)
        return f'{action} the {prod}', f'{action}ed {prod}'

    @staticmethod
    def _get_action(action_list: List[str]) -> str:
        return choice(action_list)

    @staticmethod
    def _pair_up(
            sequence: List[str]
    ) -> Tuple[List[Tuple[str, str]], Optional[str]]:
        """Break sequence into pairs."""
        part_1, part_2 = (sequence[0:len(sequence) // 2],
                          sequence[len(sequence) // 2:])
        pairs = list(zip_longest(part_1, part_2))
        remain = None if None not in pairs[-1]\
            else pairs[-1][0] or pairs[-1][1]
        if remain:
            pairs = pairs[:-1]
        return pairs, remain

    @staticmethod
    def _list_to_str(seq: list, delim: str = ', ', cap: bool = True) -> str:
        string = delim.join([item[0] for item in seq])
        if cap:
            string = string.capitalize()
        return string
