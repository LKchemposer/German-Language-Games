from abc import ABC, abstractmethod

from genderdeterminator import GenderDeterminator
from pattern import de


class Gender(ABC):
    '''Methods inferring the gender of a noun.'''

    @abstractmethod
    def get_gender(self, noun: str):
        pass


class GenderDet_Gender(Gender):
    '''Uses genderdeterminator package.'''

    def __init__(self):
        self.engine = GenderDeterminator()

    def get_gender(self, noun: str) -> str:
        gender = self.engine.get_gender(noun)
        return gender


class Pattern_Gender(Gender):
    '''Uses pattern package.'''

    @staticmethod
    def get_gender(noun: str) -> str:
        gender = de.gender(noun)
        return gender


class Ensemble_Gender(Gender):
    '''Uses an ensemble method.'''

    def __init__(self):
        self.genderdet = GenderDet_Gender()
        self.pattern = Pattern_Gender()

    def get_gender(self, noun: str) -> str:
        gender_gd = self.genderdet.get_gender(noun)
        gender_p = self.pattern.get_gender(noun)

        if gender_gd == gender_p:
            return gender_gd
        else:
            return  # raise Exception
