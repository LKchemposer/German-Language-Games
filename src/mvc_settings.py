from typing import Any
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
    def format_options(settings: dict) -> str:
        '''Format current settings.'''
        options = [f'{v.name}: {v.value}' for v in settings.values()]
        return options

    @staticmethod
    def show_settings_saved() -> None:
        '''Confirms saved settings.'''
        print('Settings saved.')


class SettingsController(Controller):

    def __init__(self, view: View = SettingsView(), model: Model = Settings()) -> None:
        super().__init__(view, model)

    def run(self) -> None:
        '''Loops showing current settings until backing to Menu or choosing a setting to change'''
        self.input_loop('', self.model.settings, self.set_setting, autoupdate=True, update_func=self.update_prompt)

    def set_setting(self, setting: Setting) -> None:
        '''Sets setting to input value.'''
        prompt = f'set {setting.name}'
        if setting.set_hint:
            prompt += f' ({setting.set_hint})'
        prompt = self.view.show_prompt(prompt, setting.options)
        value = self.input_loop_set_setting(prompt, setting)
        setting.value = value

    def update_prompt(self) -> str:
        '''Updates prompt per current settings.'''
        options = self.view.format_options(self.model.settings)
        prompt = self.view.show_prompt('Settings', options, ['or Q to go back to Menu'])
        return prompt

    def input_loop_set_setting(self, prompt: str, setting: Setting) -> Any:
        '''Loops set setting until choosing a valid input, defined in the Setting class.'''
        value = None
        while value is None:
            key = input(prompt)
            if self.quit(key):
                break
            value = setting.set_value(key)
            if value is None:
                self.view.show_try_again()
        return value

    def end(self):
        self.view.show_settings_saved()
