from mvc import Controller, Model, View
from mvc_play import PlayController
from mvc_settings import SettingsController


class MenuView(View):

    @staticmethod
    def exit_message():
        print('Thanks for playing!')


class Menu(Model):

    menu = {
        'Play': PlayController(),
        'Settings': SettingsController()
    }


class MenuController(Controller):

    def __init__(self, view: MenuView, model: Menu):
        super().__init__(view, model)

    def run(self):
        prompt = self.view.show_options(self.model.menu, 'German Language Games', ['or Q to quit'])
        self.input_loop(prompt, self.model.menu, self.run_item)

    @staticmethod
    def run_item(item):
        item.run()
        item.end()

    def end(self):
        self.view.exit_message()
