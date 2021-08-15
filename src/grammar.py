from conjadj import ConjAdj, Pattern_ConjAdj
from conjart import ConjArt, Lookup_ConjArt
from conjverb import ConjVerb, Pattern_ConjVerb
from gender import Gender, GenderDet_Gender


class Grammar():
    '''Deals with grammar-related actions (e.g., conjugation, declination, etc.).'''

    pronouns = {
        'ich': (1, 'sg'),
        'du': (2, 'sg'),
        'er': (3, 'sg'),
        'sie (sg)': (3, 'sg'),
        'es': (3, 'sg'),
        'wir': (1, 'pl'),
        'ihr': (2, 'pl'),
        'sie (pl)': (3, 'pl'),
        'Sie': (3, 'pl')
    }
    cases = ['nominative', 'accusative', 'dative', 'genitive']
    der_words = ['der', 'dies', 'jed', 'jen', 'manch', 'solch', 'welch', 'all']
    ein_words = ['ein', 'kein', 'dein', 'sein', 'ihr', 'unser', 'euer', 'Ihr']
    tenses = ['present']  # past
    conjart_options = None

    @staticmethod
    def get_gender(noun: str, method: Gender = GenderDet_Gender()) -> str:
        '''Gets inferred gender.'''
        gender = method.get_gender(noun)
        return gender

    @staticmethod
    def get_conjart(gender: str, form: str, case: str, method: ConjArt = Lookup_ConjArt()) -> str:
        '''Gets declined article.'''
        conjart = method.get_conjart(gender, form, case)
        return conjart

    def get_conjverb(self, verb: str, pronoun: str,
                     tense: str = 'present', method: ConjVerb = Pattern_ConjVerb()) -> str:
        '''Gets declined form of the verb.'''
        conjverb = method.get_conjverb(verb, tense, self.pronouns[pronoun])
        return conjverb

    def get_conjadj(self, adj: str, gender: str, case: str, form: str, method: ConjAdj = Pattern_ConjAdj()) -> str:
        '''Gets the declined form of the adjective.'''
        der_ein = self.decode_der_ein(form)  # pattern only accepts 'der' or 'ein'
        conjadj = method.get_conjadj(adj, gender, case, der_ein)
        return conjadj

    def get_conjarts(self, form: str) -> set:
        '''Get all declined articles for a determiner.'''
        if not self.conjart_options:
            lookup = Lookup_ConjArt()
            articles = lookup.articles
            self.conjart_options = {
                f: set([article for d in articles[f].values()
                       for article in d.values()])
                for f in self.der_words + self.ein_words
            }
        options = self.conjart_options[form]
        return options

    def decode_der_ein(self, form: str) -> str:
        '''Decodes the form of der or ein word.'''
        if form in self.der_words:
            return 'der'
        elif form in self.ein_words:
            return 'kein'
        else:
            return
