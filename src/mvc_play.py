from games import ConjugateVerb, ConjugateArticle, ConjugateAdjective, TranslatePfVerbs
from mvc import Controller, Model, View
from mvc_game import Game, GameController, GameView


class PlayView(View):

    @staticmethod
    def format_options(games: dict):
        options = [v.name for v in games.values()]
        return options


class Play(Model):

    games = {
        'conjugate_article': ConjugateArticle(),
        'conjugate_verb': ConjugateVerb(),
        'conjugate_adj': ConjugateAdjective(),
        'translate_pfverb': TranslatePfVerbs()
    }


class PlayController(Controller):

    def __init__(self, view=PlayView(), model=Play()):
        super().__init__(view, model)

    def run(self):
        options = self.view.format_options(self.model.games)
        prompt = self.view.show_options(
            options, 'Choose a Game:', ['or Q to quit'])
        self.input_loop(prompt, self.model.games, self.run_game)

    @staticmethod
    def run_game(game: Game):
        control = GameController(GameView(), game)
        control.run()
        control.end()

    def end(self):
        pass
