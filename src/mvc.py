from abc import ABC, abstractmethod


class Model(ABC):
    '''Handles data abstractions.'''
    pass


class View(ABC):
    '''Handles formatting and displaying messages.'''

    def show_options(self, options: list, core_msg: str, post_msgs=[]) -> str:
        '''Shows options to player.'''
        opts = [f'({i}) {option}' for i, option in enumerate(options, 1)]

        lines = [self.sep(len(core_msg)), core_msg]
        lines.extend(opts)
        lines.extend(post_msgs)
        lines.append('')

        prompt = '\n'.join(lines)
        return prompt

    @staticmethod
    def sep(width: int, ch: str = '='):
        return ch * width


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
    def quit(input_, quits=['q', 'quit', 'exit']) -> bool:
        '''Checks if user wants to quit.'''
        return input_.strip().lower() in quits

    def input_loop(self, prompt: str, options: dict, func, autoupdate: bool = False, update_func=None):
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
                print('Try again!')
