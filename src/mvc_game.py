import random
import textwrap
from abc import ABC, abstractmethod
from typing import Tuple

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

    default_loads = {
        'nouns': 'load_duolingo',
        'verbs': 'load_duolingo',
        'adjectives': 'load_duolingo',
        'pfverbs': 'load_pfverbs_csv'
    }

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

    def refine_options(self, opts: list, answer: str) -> list:
        '''Refines number of options to n_options, and shuffles.'''
        all_ = list(opts)
        all_.remove(answer)

        n_options = self.settings.settings['n_options'].value - 1
        no_ans = random.sample(all_, k=min(n_options, len(all_)))

        options = no_ans + [answer]
        random.shuffle(options)
        return options

    def load_default(self, pos: str) -> None:
        '''Loads database.'''
        method = getattr(self.database, self.default_loads[pos])
        try:
            self.database.load_vocab_json()
            if not getattr(self.database, pos):
                method()
        except (FileNotFoundError, FileExistsError):
            method()

        finally:
            self.database.save_vocab_json()


class GameView(View):

    @staticmethod
    def show_check(is_correct: bool, answer: str) -> None:
        '''Congrats or displays answer if wrong.'''
        if is_correct:
            print('Nice! Next')
        else:
            print(f'Sorry. Answer: {answer}')

    @staticmethod
    def show_end_score(success) -> None:
        '''Displays score at the end of the game.'''
        print(f'Too bad. Game over! ⭑ {success}')

    @staticmethod
    def show_score(success, **kwargs) -> None:
        '''Displays score.'''
        print(f'⭑ {success}', **kwargs)

    @staticmethod
    def show_life(life, **kwargs) -> None:
        '''Displays lives left.'''
        print(f'❤️ {life}', **kwargs)

    @staticmethod
    def format_answer(answer: str, options: list = []) -> str:
        '''Formats the answer to be compared with guess, depending on multiple choice mode.'''
        if options:
            options = {
                option: i for i, option in enumerate(options, 1)
            }
            return str(options[answer])
        return answer

    def show_name(self, game: Game) -> None:
        '''Displays name of the game.'''
        print(game.name, self.sep(len(game.name)), sep='\n')

    @staticmethod
    def show_instruction(game: Game, **kwargs) -> None:
        '''Displays instruction for the game.'''
        print(textwrap.fill(game.instruction, **kwargs))

    @staticmethod
    def show_example(game: Game) -> None:
        '''Displays an example for the game.'''
        print(f'Example: {game.example}')


class GameController(Controller):

    def __init__(self, view: View, game: Game) -> None:
        super().__init__(view, game)
        self.settings = Settings()
        self.life = self.settings.settings['life'].value
        self.success = 0

    def run(self) -> None:
        '''Runs the game until no lives left.'''
        self.view.show_name(self.model)
        self.view.show_instruction(self.model)
        self.view.show_example(self.model)

        while self.life > 0:
            self.view.show_life(self.life, end='\t')
            self.view.show_score(self.success)

            answer, prompt = self.generate_answer_prompt()

            guess = input(prompt)
            if self.quit(guess):
                break

            is_correct = self.check_answer(guess, answer)
            self.view.show_check(is_correct, answer)

    def end(self) -> None:
        self.view.show_end_score(self.success)

    def check_answer(self, guess: str, answer: str) -> bool:
        '''Checks guess against answer.'''
        is_correct = guess == answer
        if is_correct:
            self.success += 1
        else:
            self.life -= 1
        return is_correct

    def generate_answer_prompt(self) -> Tuple[str]:
        '''Generates and formats answer and prompt.'''
        multiple_choice = self.settings.settings['multiple_choice'].value

        self.model.generate_question()
        answer = self.model.generate_answer()
        options = self.model.generate_options() if multiple_choice else []
        prompt = self.model.generate_prompt()

        answer = self.view.format_answer(answer, options)
        prompt = self.view.show_prompt(prompt, options)

        return answer, prompt
