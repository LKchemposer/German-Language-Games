from abc import ABC, abstractmethod

from pattern import de


class ConjVerb(ABC):
    '''Methods to conjugate verb.'''

    @abstractmethod
    def get_conjverb():
        pass


class Pattern_ConjVerb(ConjVerb):
    '''Uses pattern package.'''

    @staticmethod
    def get_conjverb(verb: str, tense: str, pronoun: tuple):
        conjverb = de.conjugate(verb, tense, *pronoun)
        return conjverb
