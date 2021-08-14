import random
import textwrap
from abc import ABC, abstractmethod

from database import Database
from grammar import Grammar
from mvc import Controller, Model, View
from mvc_settings import Settings


class Game(Model, ABC):

    grammar = Grammar()
    database = Database()
    settings = Settings()
    name: str
    instruction: str
    example: str

    @abstractmethod
    def generate_question():
        pass

    @abstractmethod
    def generate_answer():
        pass

    @abstractmethod
    def generate_prompt():
        pass

    @abstractmethod
    def generate_options():
        pass

    def refine_options(self, opts, answer: str) -> list:
        '''Refines number of options to n_options, and shuffles.'''
        all_ = list(opts)
        all_.remove(answer)

        n_options = self.settings.settings['n_options'].value - 1
        no_ans = random.sample(all_, k=min(n_options, len(all_)))

        options = no_ans + [answer]
        random.shuffle(options)
        return options

    def load_default(self):
        print('Loading verbs, nouns, adjectives...')
        try:
            self.database.load_vocab_json()
        except FileNotFoundError:
            print('No vocab data found. Loading from Duolingo...')
            self.database.load_duolingo()
            print('Load vocab data from Duolingo completed!')
        print('Saving vocab data to local machine...')
        self.database.save_vocab_json()


class GameView(View):

    @staticmethod
    def check_message(is_correct: bool, answer: str):
        '''Handles messaging when checking answer.'''
        if is_correct:
            print('Nice! Next')
        else:
            print(f'Sorry. Answer: {answer}')

    @staticmethod
    def show_end_score(success):
        '''Displays score at the end of the game.'''
        print(f'Too bad. Game over! ⭑ {success}')

    @staticmethod
    def show_score(success, **kwargs):
        '''Displays score.'''
        print(f'⭑ {success}', **kwargs)

    @staticmethod
    def show_life(life, **kwargs):
        '''Displays lives left.'''
        print(f'❤️ {life}', **kwargs)

    @staticmethod
    def format_answer(answer: str, multiple_choice: bool, options: list) -> str:
        '''Formats the answer to be compared with guess.'''
        if multiple_choice:
            options = {
                option: i for i, option in enumerate(options, 1)
            }
            return str(options[answer])
        return answer

    def format_prompt(self, core_msg: str, multiple_choice: bool, options: list) -> str:
        '''Formats the prompt to be displayed.'''
        prompt = self.show_options(
            options, core_msg) if multiple_choice else f'{core_msg}: '
        return prompt

    @staticmethod
    def show_instruction(instruction, **kwargs):
        print(textwrap.fill(instruction, **kwargs))

    @staticmethod
    def show_example(example):
        print(f'Example: {example}')

    def show_name(self, name):
        print(name, self.sep(len(name)), sep='\n')


class GameController(Controller):

    def __init__(self, view: View, game: Game):
        super().__init__(view, game)
        self.settings = Settings()
        self.life = self.settings.settings['life'].value
        self.success = 0

    def run(self):
        '''Runs the game until no lives left.'''
        self.view.show_name(self.model.name)
        self.view.show_instruction(self.model.instruction)
        self.view.show_example(self.model.example)

        while self.life > 0:
            self.view.show_life(self.life, end='\t')
            self.view.show_score(self.success)

            answer, prompt = self.generate_answer_prompt()

            guess = input(prompt)
            if self.quit(guess):
                break

            is_correct = self.check_answer(guess, answer)
            self.view.check_message(is_correct, answer)

    def end(self):
        self.view.show_end_score(self.success)

    def check_answer(self, guess, answer):
        '''Checks guess against answer.'''
        is_correct = guess == answer
        if is_correct:
            self.success += 1
        else:
            self.life -= 1
        return is_correct

    def generate_answer_prompt(self):
        '''Generates and formats answer and prompt.'''
        multiple_choice = self.settings.settings['multiple_choice'].value

        self.model.generate_question()
        answer = self.model.generate_answer()
        options = self.model.generate_options() if multiple_choice else None
        prompt = self.model.generate_prompt()

        answer = self.view.format_answer(answer, multiple_choice, options)
        prompt = self.view.format_prompt(prompt, multiple_choice, options)

        return answer, prompt
