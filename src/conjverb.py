from abc import ABC, abstractmethod

from pattern import de


class ConjVerb(ABC):
    '''Methods to decline the conjugated form of a verb, given a tense, and pronoun.'''

    @staticmethod
    @abstractmethod
    def get_conjverb():
        pass


class Pattern_ConjVerb(ConjVerb):
    '''Uses pattern package.'''

    @staticmethod
    def get_conjverb(verb: str, tense: str, pronoun: tuple) -> str:
        conjverb = de.conjugate(verb, tense, *pronoun)
        return conjverb
