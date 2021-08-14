from mvc import Controller, Model, View
from settings import Setting, Life, MultipleChoice, n_Options


class Settings(Model):

    settings = {
            'multiple_choice': MultipleChoice(True),
            'n_options': n_Options(3),
            'life': Life(3)
        }


class SettingsView(View):

    @staticmethod
    def format_options(settings: dict):
        options = [f'{v.name}: {v.value}' for v in settings.values()]
        return options

    @staticmethod
    def settings_saved():
        print('Settings saved.')


class SettingsController(Controller):

    def __init__(self, view=SettingsView(), model=Settings()):
        super().__init__(view, model)

    def run(self):
        self.input_loop('', self.model.settings, self.set_setting,
                        autoupdate=True, update_func=self.update_prompt)

    def set_setting(self, setting: Setting):
        value = getattr(self, setting.method)(setting)
        setting.value = value

    def update_prompt(self):
        options = self.view.format_options(self.model.settings)
        prompt = self.view.show_options(
            options, 'Settings', ['or Q to go back to Menu'])
        return prompt

    def choose_one(self, setting: Setting):
        prompt = self.view.show_options(setting.options, f'set {setting.name}')
        value = self.input_loop_set_setting(prompt, options=setting.options)
        return value

    def fill_in(self, setting: Setting):
        prompt = f'set {setting.name}: '
        value = self.input_loop_set_setting(
            prompt, condition=setting.is_valid)
        return value

    def input_loop_set_setting(self, prompt: str, options=[], condition=None):
        value = None
        while value is None:
            key = input(prompt)
            if self.quit(key):
                break
            if options and key.isdigit() and int(key) - 1 in range(len(options)):
                value = options[int(key) - 1]
            elif condition(key):
                value = int(key)
            else:
                print('Try again!')
        return value

    def end(self):
        self.view.settings_saved()
