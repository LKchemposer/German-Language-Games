import json
from abc import ABC, abstractmethod

from pattern import de


class Article(ABC):
    '''Methods declining article from the gender and case of a noun.'''

    @abstractmethod
    def get_conjart(self, gender: str, case: str):
        pass


class Pattern_Article(Article):
    '''Uses pattern package.'''

    @staticmethod
    def get_conjart(gender: str, definite: str, case: str):
        conjart = de.article('', function=definite, gender=gender, role=case)
        return conjart


class Lookup_Article(Article):
    '''Looks up article from a json file.'''

    def __init__(self, article_path: str = '../data/articles.json'):
        with open(article_path, 'r') as js:
            self.articles = json.load(js)

    def get_conjart(self, gender: str, form: str, case: str):
        conjart = self.articles.get(form, dict()).get(case, dict()).get(gender)
        if not conjart:
            return  # raise form, case, or gender does not exist in json file
        return conjart
