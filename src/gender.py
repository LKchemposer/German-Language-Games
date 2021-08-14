from abc import ABC, abstractmethod

from genderdeterminator import GenderDeterminator
from pattern import de


class Gender(ABC):
    '''Methods inferring the gender of a noun.'''

    @abstractmethod
    def get_gender():
        pass


class GenderDet_Gender(Gender):
    '''Uses genderdeterminator package.'''

    @staticmethod
    def get_gender(noun: str) -> str:
        gender = GenderDeterminator().get_gender(noun)
        return gender


class Pattern_Gender(Gender):
    '''Uses pattern package.'''

    @staticmethod
    def get_gender(noun: str) -> str:
        gender = de.gender(noun)
        return gender
