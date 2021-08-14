from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class Setting():
    value: Any
    name: str
    method: str
    options: List[bool] = field(default_factory=list)


@dataclass
class MultipleChoice(Setting):

    value: bool
    name: str = 'Multiple Choice?'
    method: str = 'choose_one'

    def __post_init__(self):
        self.options = [True, False]

    def is_valid(self, v):
        return v.isdigit() and int(v) - 1 in range(len(self.options))


@dataclass
class n_Options(Setting):

    value: int
    name: str = 'Number of Options (in Multiple Choice)'
    method: str = 'fill_in'

    @staticmethod
    def is_valid(v):
        return v.isdigit() and int(v) in range(2, 11)


@dataclass
class Life(Setting):

    value: int
    name: str = 'Number of Lives'
    method: str = 'fill_in'

    @staticmethod
    def is_valid(v):
        return v.isdigit() and int(v) in range(1, 11)


# class ArticleMode(Setting):
#     def __init__(self, value) -> None:
#         super().__init__(value)
#         self.name = 'Article Mode'
#         self.method = 'choose_one'
#         self.options = [
#             'der/die/das and (k)ein only', 'all der words and ein words']
#         self.condition = lambda v: v.isdigit() and int(v) - 1 in range(len(self.options))


# class Cases(Setting):
#     def __init__(self, value) -> None:
#         super().__init__(value)
#         self.name = 'Cases'
#         self.method = 'choose_multiple'
#         self.options = ['nominative', 'accusative', 'dative', 'genitive']
#         self.condition = None


# class Tenses(Setting):
#     def __init__(self, value) -> None:
#         super().__init__(value)
#         pass
