from abc import ABC, abstractmethod


class Setting(ABC):
    name: str
    method: str
    options: list

    @abstractmethod
    def __init__(self, value) -> None:
        self.value = value


class MultipleChoice(Setting):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.name = 'Multiple Choice?'
        self.method = 'choose_one'
        self.options = [True, False]
        self.condition = lambda v: v.isdigit() and int(v) - 1 in range(len(self.options))


class n_Options(Setting):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.name = 'Number of Options (in Multiple Choice)'
        self.method = 'fill_in'
        self.options = []
        self.condition = lambda v: v.isdigit() and int(v) in range(2, 11)


class Life(Setting):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.name = 'Number of Lives'
        self.method = 'fill_in'
        self.options = []
        self.condition = lambda v: v.isdigit() and int(v) in range(1, 11)


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
