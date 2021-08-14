import json
from abc import ABC, abstractmethod

from pattern import de


class ConjArt(ABC):
    '''Methods declining article, given the form (der/ein words), case (e.g., nominative), and gender of the noun.'''

    @staticmethod
    @abstractmethod
    def get_conjart():
        pass


class Pattern_ConjArt(ConjArt):
    '''Uses pattern package.'''

    @staticmethod
    def get_conjart(gender: str, form: str, case: str) -> str:
        conjart = de.article('', function=form, gender=gender, role=case)
        return conjart


class Lookup_ConjArt(ConjArt):
    '''Looks up article from a json file.'''

    def __init__(self, article_path: str = '../data/articles.json'):
        with open(article_path, 'r') as js:
            self.articles = json.load(js)

    def get_conjart(self, gender: str, form: str, case: str) -> str:
        conjart = self.articles[form][case][gender]
        return conjart
