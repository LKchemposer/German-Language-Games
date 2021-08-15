from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class Setting(ABC):
    value: Any
    name: str
    set_hint: str = ''
    options: List[bool] = field(default_factory=list)

    @abstractmethod
    def set_value():
        pass


@dataclass
class MultipleChoice(Setting):

    value: bool
    name: str = 'Multiple Choice?'

    def __post_init__(self):
        self.options = [True, False]

    def set_value(self, v):
        if v.isdigit() and int(v) - 1 in range(len(self.options)):
            return self.options[int(v) - 1]
        else:
            return


@dataclass
class n_Options(Setting):

    value: int
    name: str = 'Number of Options (in Multiple Choice)'
    set_hint: str = '2-10'

    @staticmethod
    def set_value(v):
        if v.isdigit() and int(v) in range(2, 11):
            return int(v)
        else:
            return


@dataclass
class Life(Setting):

    value: int
    name: str = 'Number of Lives'
    set_hint: str = '1-10, or unlimited'

    @staticmethod
    def set_value(v):
        if v == 'unlimited':
            return 9999
        elif v.isdigit() and int(v) in range(1, 11):
            return int(v)
        else:
            return


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
