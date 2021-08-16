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
* MVC
    * Model: grammar, database, games
    * View: game UI
    * Controller: event handling

### Classes
* [x] Database: loads, saves list or dict of nouns, verbs, etc.

* [x] Grammar: hub for grammar-related actions: conjugation, declination, etc.
    * Gender: get gender from noun
        * GenderDet
        * Linguee
        * Pattern
    * Article
        * Pattern: only outputs der/die/das and ein
        * Lookup: search a dict
            * form: der/die/das, dies-, solch-, kein-, mein-, etc.
    * VerbConj
        * Pattern

* [x] Game: define what games should output, shared methods across all games
    * **abstract**: generate question, answer, prompt, options
    * ConjugateArticle
        * generate_question: random noun, form, case
        * generate_answer: conjart
        * generate_prompt: `"(solch) Maus"`
        * generate_options:
            * grammar calls Lookup, get articles
            * set of articles per form
    * ConjugateVerb
        * generate_question: random pronoun (grammar), verb
        * generate_answer: conjverb
        * generate_prompt: `"ich (sein)"`
        * generate_options:
            * conjverb for all pronouns
    * ConjugateAdjective
        * calls ConjugateArticle
        * generate_question:
            * conjart.generate_question -> noun, form, case
            * conjart.generate_answer -> article
        * generate_answer -> conjadj
            * grammar decode der_words and ein_words, req. for pattern
        * generate_prompt: `"eine/unsere (schön) Frau"` or `"die/solche (schön) Frau"` or `"(schön) Frau"`
        * generate_options:
            * set of representative adjective forms?
                * nominative-m-der: -e
                * accusative-m-der: -en
                * nominative-m-ein: -er
                * nominative-n-ein: -es
                * dative-m-'': -em
    * TranslatePfVerbs
        * generate_question: random pfverb
        * generate_answer: `pfverbs['meaning']`
        * generate_prompt: `"beginnen"`
        * generate_options: random meanings
    * [ ] PickSynonyms: TBD


* [x] MVCs
    * C
        * **abstract methods:** run, end
        * input loop
    * MenuView, Menu, MenuController: Play or Settings
    * PlayView, Play, PlayController: show games
    * SettingsView, Settings, SettingsController: set settings
    * GameView, Game, GameController: runs the game
        * GC
            * Loops generate question, answer, etc.
            * Check answer


* [x] Settings: set game params
    * [x] lives, n_options for multiple choice
    * [ ] grammar
        * cases
        * der words
        * ein words

### 3rd Parties

* genderdeterminator
    * gender
* pattern de
    * gender
    * attributive adjective
    * conjugate verb
* Linguee API
    * genders

## Testing & Security

### Unit Testing

* [ ] Database: loading, saving
    * [ ] load_duolingo
        * no connection
        * wrong username password
    * processing - TBD: to be changed for better parsing of nouns
    * [ ] load_pfverbs
        * path doesn't exist
        * empty file
        * check having column headings: base, prefix, meaning
    * [ ] save_vocab_json
        * path doesn't exist
        * file already exist -> replace
    * [ ] load_vocab_json
        * path doesn't exist
        * json not giving a dict()

* [ ] Grammar: get methods, unexpected inputs, etc.
    * [ ] get_gender, get_conjart, get_conjverb, get_conjadj
        * method doesn't have get_ methods
    * [ ] get_conjarts
        * empty (form)
        * check articles
            * is a nested dict()
            * having at least form str as key
        * check form is in der_words and ein_words
        * check output is a set
    * [ ] decode_der_ein
        * typo (form) -> output not None

    * [ ] get_ methods of implementations of Gender(), ConjArt(), ConjVerb(), ConjAdj()
        * correct
        * empty
        * typo
        * digits
        * case

    * [ ] **special:** LookUp_Article()
        * loading
            * path doesn't exist
            * json not giving a nested dict()

* Input (MVCs)
    * [ ] mvc
        * show_prompt
        * sep
        * show_try_again
        * quit
        * input_loop

    * [ ] general mvc
        * controller init
        * run()
        * end()

    * [ ] menu
        * exit_message
        * run_item
    * [ ] play
        * format_options
        * run_game()
    * [ ] game
        * refine_options
        * load_default
        * show_check
        * show_end_score, show_score, show_life
        * show_name, show_instruction, show_example
        * check_answer
        * generate_answer_prompt
   
        

* Games
    * 

* [ ] Settings: set settings
    * [ ] view
        * format_options
        * show_settings_saved

    * [ ] controller
        * set_setting
        * update_prompt
        * input_loop_set_setting

## Deployment

* GitHub package?

## Planning

* Required
    * [x] Functional games
    * [x] Decently accurate? grammar
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
* [x] Docstring, type hints
* [x] Update UML
* [ ] Error handling
* [ ] Unit testting
* [ ] Github