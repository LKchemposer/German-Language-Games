from abc import ABC, abstractmethod
from typing import Iterable


class Model(ABC):
    '''Handles data abstractions and transformations.'''
    pass


class View(ABC):
    '''Handles formatting and displaying messages.'''

    def show_prompt(self, core_msg: str, options: list = [], post_msgs: list = []) -> str:
        '''Shows options to user.'''
        if options:
            opts = [f'({i}) {option}' for i, option in enumerate(options, 1)]

            lines = [self.sep(len(core_msg)), core_msg]
            lines.extend(opts)
            lines.extend(post_msgs)
            lines.append('')

            prompt = '\n'.join(lines)
        else:
            prompt = f'{core_msg}: '
        return prompt

    @staticmethod
    def sep(width: int, ch: str = '='):
        '''Adds a separator'''
        return ch * width

    @staticmethod
    def show_try_again():
        print('Try again')


class Controller(ABC):
    '''Controls View and Model, and handles input by user.'''

    @abstractmethod
    def __init__(self, view: View, model: Model):
        self.view = view
        self.model = model

    @abstractmethod
    def run():
        pass

    @abstractmethod
    def end():
        pass

    @staticmethod
    def quit(input_: str, quits: list = ['q', 'quit', 'exit']) -> bool:
        '''Checks if user wants to quit.'''
        return input_.strip().lower() in quits

    def input_loop(self, prompt: str, options: Iterable, func, autoupdate: bool = False, update_func=None):
        '''Loops input until a valid option is given, in which case, func is called.'''
        while True:
            if autoupdate:
                prompt = update_func()

            key = input(prompt)

            if self.quit(key):
                break

            if key.isdigit() and int(key) - 1 in range(len(options)):
                item = options[list(options)[int(key) - 1]]
                func(item)

            else:
                self.view.show_try_again()
