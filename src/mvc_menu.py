from mvc import Controller, Model, View
from mvc_play import PlayController
from mvc_settings import SettingsController


class MenuView(View):

    @staticmethod
    def exit_message() -> None:
        '''Displays exit message.'''
        print('Thanks for playing!')


class Menu(Model):

    menu = {
        'Play': PlayController(),
        'Settings': SettingsController()
    }


class MenuController(Controller):

    def __init__(self, view: MenuView, model: Menu):
        super().__init__(view, model)

    def run(self) -> None:
        '''Loops Menu until choosing an option or quitting.'''
        prompt = self.view.show_prompt('German Language Games', self.model.menu, ['or Q to quit'])
        self.input_loop(prompt, self.model.menu, self.run_item)

    @staticmethod
    def run_item(item) -> None:
        '''Runs Play or Settings.'''
        item.run()
        item.end()

    def end(self) -> None:
        self.view.exit_message()
