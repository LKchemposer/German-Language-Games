import random

from mvc_game import Game


class ConjugateArticle(Game):
    '''Decline the correct form of the article for a noun, given case.'''

    def __init__(self) -> None:
        self.name = 'Conjugate the Article'
        self.instruction = self.__doc__
        self.example = '(der) Frau - accusative -> die'

    def load_nouns(self) -> None:
        'Loads in nouns from database.'
        if not self.database.nouns:
            self.load_default()
        self.nouns = self.database.nouns

    def generate_question(self) -> None:
        '''Generates a random noun, article's der word or ein word, and case.'''
        self.load_nouns()

        self.n = random.randrange(len(self.nouns))
        self.noun = self.nouns[self.n]['noun']
        # option to turn word into plural
        self.form = random.choice(
            self.grammar.der_words + self.grammar.ein_words)
        self.case = random.choice(self.grammar.cases)

    def generate_answer(self) -> str:
        '''Generates the answer (the article) using Grammar.'''
        self.gender = self.nouns[self.n].get('gender')
        if not self.gender:
            self.gender = self.grammar.get_gender(self.noun)

        self.conjart = self.grammar.get_conjart(
            self.gender, self.form, self.case)
        return self.conjart

    def generate_prompt(self) -> str:
        '''Generates the core message of the prompt.'''
        prompt = f'({self.form}) {self.noun.title()} - {self.case}'
        return prompt

    def generate_options(self) -> list:
        '''Generates options for multiple choice.'''
        forms = self.grammar.get_conjart_options(self.form)
        options = self.refine_options(forms, self.conjart)
        return options


class ConjugateVerb(Game):
    '''Decline the correct conjugated form of the verb.'''

    def __init__(self) -> None:
        self.name = 'Conjugate the Verb'
        self.instruction = self.__doc__
        self.example = 'er (sein) -> ist'

    def load_verbs(self) -> None:
        'Loads in verbs from database.'
        if not self.database.verbs:
            self.load_default()
        self.verbs = self.database.verbs

    def generate_question(self) -> None:
        'Select a random verb and pronoun.'
        self.load_verbs()
        self.verb = random.choice(self.verbs)
        self.pronoun = random.choice(list(self.grammar.pronouns))

    def generate_answer(self) -> str:
        '''Generates answer (the conjugated form) using Grammar.'''
        self.conjverb = self.grammar.get_conjverb(self.verb, self.pronoun)
        return self.conjverb

    def generate_prompt(self) -> str:
        '''Generates the core message of the prompt.'''
        prompt = f'{self.pronoun} ({self.verb})'
        return prompt

    def generate_options(self) -> list:
        '''Generates options for multiple choice.'''
        conjverbs = set([self.grammar.get_conjverb(self.verb, pronoun)
                        for pronoun in self.grammar.pronouns])
        options = self.refine_options(conjverbs, self.conjverb)
        return options


class ConjugateAdjective(Game):
    '''Decline the correct conjugated form of the adjective for a noun, given an article and case.'''

    def __init__(self) -> None:
        self.name = 'Conjugate the Adjective'
        self.instruction = self.__doc__
        self.example = 'eine (schön) Frau -> schöne'

        self.conjugate_article = ConjugateArticle()

        self.set_cases = [
            ('m', 'nominative', 'der'),
            ('m', 'accusative', 'der'),
            ('m', 'nominative', 'kein'),
            ('n', 'nominative', 'kein'),
            ('m', 'dative', '')
        ]

    def load_adjectives(self) -> None:
        'Loads in adjectives from database.'
        if not self.database.adjectives:
            self.load_default()
        self.adjectives = self.database.adjectives

    def generate_question(self) -> None:
        'Select a random adjective, noun, article. The noun and article are randomly selected via Guess Article class.'
        self.load_adjectives()
        self.adjective = random.choice(self.adjectives)

        self.conjugate_article.generate_question()
        self.conjugate_article.generate_answer()

        self.noun = self.conjugate_article.noun
        self.case = self.conjugate_article.case
        self.form = random.choices(
            [self.conjugate_article.form, ''], weights=[2, 1])[0]

        self.gender = self.conjugate_article.gender
        self.conjart = self.conjugate_article.conjart if self.form else ''

    def generate_answer(self) -> str:
        '''Generates answer (the conjugated form) using Grammar.'''
        self.conjadj = self.grammar.get_conjadj(
            self.adjective, self.gender, self.case, self.form)
        return self.conjadj

    def generate_prompt(self) -> str:
        '''Generates the core message of the prompt.'''
        prompt = f'{self.conjart} ({self.adjective}) {self.noun.title()}'.strip()
        if not self.form:
            prompt += f' - {self.case}'
        return prompt

    def generate_options(self) -> list:
        '''Generates options for multiple choice.'''
        conjadjs = set([self.grammar.get_conjadj(self.adjective, *case)
                       for case in self.set_cases])
        options = self.refine_options(conjadjs, self.conjadj)
        return options


class TranslatePfVerbs(Game):
    '''Choose the closest English meaning of the German separable and inseparable verbs, or vice versa.'''

    def __init__(self) -> None:
        self.name = 'Translate Prefix Verbs'
        self.instruction = self.__doc__
        self.example = 'einziehen -> move in (a new apartment)'

    def load_pfverbs(self) -> None:
        'Loads in prefix verbs from database.'
        if not self.database.pfverbs:
            self.database.load_pfverbs_csv()
        self.pfverbs = self.database.pfverbs

    def generate_question(self) -> None:
        'Select a random prefix verb.'
        self.load_pfverbs()
        self.n = random.randrange(len(self.pfverbs))
        self.pfverb = self.to_pfverb(self.pfverbs, self.n)

    def generate_answer(self) -> str:
        '''Looks up meaning.'''
        self.meaning = self.pfverbs[self.n]['meaning']
        return self.meaning

    def generate_prompt(self) -> str:
        '''Generates the core message of the prompt.'''
        prompt = str(self.pfverb)
        return prompt

    def generate_options(self) -> list:
        '''Generates options for multiple choice.'''
        ns = self.refine_options(range(len(self.pfverbs)), self.n)
        options = [self.pfverbs[n]['meaning'] for n in ns]
        return options

    @staticmethod
    def to_pfverb(pfverbs: dict, n: int):
        return pfverbs[n]['prefix'] + pfverbs[n]['base']
