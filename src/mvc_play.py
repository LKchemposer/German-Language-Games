from games import ConjugateVerb, ConjugateArticle, ConjugateAdjective, TranslatePfVerbs
from mvc import Controller, Model, View
from mvc_game import Game, GameController, GameView


class PlayView(View):

    @staticmethod
    def format_options(games: dict) -> list:
        '''Formats the name of the games.'''
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

    def run(self) -> None:
        '''Loops showing the games until backing to Menu or choosing a game.'''
        options = self.view.format_options(self.model.games)
        prompt = self.view.show_prompt('Choose a Game:', options, ['or Q to quit'])
        self.input_loop(prompt, self.model.games, self.run_game)

    @staticmethod
    def run_game(game: Game) -> None:
        '''Runs the game.'''
        game_ = GameController(GameView(), game)
        game_.run()
        game_.end()

    def end(self) -> None:
        pass
