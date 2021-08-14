# Software Design

## About
* **What is it?** Collection of games to help me remember grammar rules, words, etc.
* **Who is it for?** Me, first and foremost, but should be flexible enough for other users to install and play (in v1.2?)
* **What problem does it solve?** Duolingo does not have grammar intensive exercises, online resources (e.g., Grimm Grammar) do not have many exercises of one kind; need something repetitive and customizable depending on existing vocab knowledge
* **How is it going to work?** User chooses a game to play, can be on terminal, or web app (in 1.2?)
* **Other items to consider**
    * Integrations: Duolingo vocab list, csv separable verbs
    * MVC pattern

## UI
### General UI
* Basic
    1. Ask to choose a game
    2. Options: games, quit

* Extensions
    * Options menu:
        * Set lives
        * Set params for games
    
#### Game-specific

##### Guess article
* Basic
    1. Give definiteness, case
    2. Input article
    3. If correct, continue; else, lose a life, show correct answer
    4. Repeat until dead

* Extensions
    * Multiple choice version
    * Flexible definiteness options: der-words, ein-words
    * Sentences, via NLP?

##### Conjugate verb

* Basic
    1. Give verb, pronoun
    2. Input conjugated form
    3. If correct, continue; else, lose a life, show correct answer
    4. Repeat until dead
    
* Extensions
    * Verbs can be (in)separables, need good conjugation engine
    * 3rd person pronouns sometimes replaced by nouns

##### Decline adjective

* Basic
    1. Give noun, case, article
    2. Input declined form
    3. If correct, continue; else, lose a life, show correct answer
    4. Repeat until dead

* Extensions
    * Only give noun, case, definiteness, input declined article, adjective, and noun
    * Sentences, via NLP?

##### Translate (in)separables
* Basic
    1. Give verb/meaning
    2. Choose meaning/verb (MC)
    3. If correct, continue; else, lose a life, show correct answer
    4. Repeat until dead

* Extensions
    * Self-adjusting to increase difficulty
        * Increase/decrease n options
        * Increase/decrease prob of chosen if answered incorrectly/correctly
        
##### Pick synonyms
* Basic
    1. Give word
    2. Choose synonym (MC)
    3. If correct, continue; else, lose a life, show correct answer
    4. Repeat until dead
    
* Extensions

## Tech Specs
### Concepts
* **Pattern:** MVC
    * Model
        * Grammar, Database, 
    * View
        * Game UI
    * Controller
        * Event handling

#### Classes
* Database:    
    * load_duolingo
    * load_separables

* Grammar: dealing with grammar-related actions (e.g., conjugation, declination, etc.)
    * get_gender(noun: str, method: Gender) -> str
    * get_article(gender: str, case: str, method: Article) -> str
    * get_conjverb(verb: str, pronoun: , tense, method: VerbConj) -> str
    * get_conjadj()
    
* Gender(ABC)
    * get_gender(noun) -> gender
    ===
    * GenderDet(Gender)
    * Linguee(Gender)
    * Pattern(Gender)

* Article(ABC)
    * get_article(gender, case) -> article
    ===
    * Pattern(definiteness): only outputs der/die/das and ein
    * Lookup(word_prefix): search a dict
        * word_prefix: der/die/das, dies-, solch-, kein-, mein-, etc.

* VerbConj(ABC)
    * get_conjverb(verb, pronoun, tense) -> conj
    ===
    * Pattern

    
* Game(ABC): define what games should output
    * Grammar()
    ---
    * generate_question -> question
    * generate_answer -> answer
    * (get options -> options)
    * generate_prompt -> prompt
    ===
    * GuessArticle
        * nouns
        * forms
        * cases
        ---
        * generate_question() -> noun, form, case
            * random: noun, form, case
        * generate_answer() -> article
            * to_gender(noun), to_article(noun, form, case)
        * generate_prompt() -> "(solch) Maus"
        * generate_options() -> options
            * grammar instantiates Lookup_Article, get self.articles
            * set([article for d in articles[form].values() for article in d.values()])

<!-- have not implemented -->
    ===
    * ConjugateVerb
        * verbs
        ---
        * generate_question() -> pronoun, verb
            * pronouns from self.grammar
        * generate_answer() -> conjverb
        * generate_prompt() -> "ich (sein)"
        * generate_options(n_options=3) # n_options should be set in Options Menu
            * conjs = set([conjverb(verb, pronoun) for pronoun in pronouns])
            * random.choices(conjs, n_options)
    ===
    * DeclineAdjective
        * adjectives
        * init -> g_article = GuessArticle(nouns)
        ---
        * generate_question() -> noun, article [der_word, ein_word, ''] , adjective
            * g_article.generate_question() -> noun, form, case
            * g_article.generate_answer() -> article
        * generate_answer() -> conjadj
            * self.grammar.get_conjadj(adjective, gender, role, article)
            * grammar decode der_words and ein_words
        * generate_prompt() -> "eine/unsere (schön) Frau" or "die/solche (schön) Frau" or "(schön) Frau"
        * generate_options(n_options=3) -> conjadj(adjective, *) for
            * set of representative adjective forms?
                * nominative-m-der: -e
                * accusative-m-der: -en
                * nominative-m-ein: -er
                * nominative-n-ein: -es
                * dative-m-'': -em
    ===
    * TranslateInSeparables
    ===
    * PickSynonyms

<!-- have not implemented -->
       
* GameView(View): game UI
    * controller: Controller
    ---
    * show_prompt():
    * show_score():
    * show_life():

* MenuView(View): menu UI
    * controller: Controller
    ---
    * show_games():

* Controller(ABC):    
    * run()
    * end()
    ===
    * MenuController(Controller): handle controls of menu
        * database: Database, view: View
        ---
        * run():
            * load Duolingo, separables into Database
            * load Grammar
            * view.show_games()
            * input loop
            * GameController(game)
            * if break, end() 
        * end():
    ===
    * GameController(Controller): handle controls of the game
    * database: Database, grammar: Grammar, view: View
    * game: Game, life: int, success: int = 0
    ---
    * run(life, game):
        * while life > 0, G = game(database, grammar)
        * G.get_answer()
        * G.get_prompt(), view.show_prompt()
        * ask for input
        * check_answer()
        * if break, end()
    * end()
        * view.show_score()
    * check_answer(guess, answer)
        * if correct, success += 1
        

* Options: set game params
    * lives
    * n_options for multiple choice
    * grammar
        * cases
        * der words
        * ein words

### 3rd Parties
* Linguee API
    * Noun genders
    
* `genderdeterminator`
    * Noun genders

* `pattern de`
    * 

## Testing & Security
* 

## Deployment

* GitHub

## Planning

* Required
    * [x] Functional games
    * [x] Decently accurate
* Optional
    * [ ] Pluralization
    * [ ] Option to include pfverbs in Conjugate Verbs
    * [ ] EN-DE mode for Translate PfVerbs
    * [ ] More detailed explanation when wrong
    * [ ] Various levels of vocab
    * [ ] More customizable settings

# To Do
* [x] Finish Settings
* [x] Refactor Controller into template
* [x] Implement DeclineAdj, TranslateSeparables
* [ ] Docstring, type hints
* [ ] Update UML
* [ ] Error handling
* [ ] Unit testting
* [ ] Github