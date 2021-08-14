import json


def create_articles_json():
    '''Create hashmap of declined forms for der- and ein- words as a json.'''

    # der/die/das irregular
    articles = {
        'der': {
            'nominative': {
                'm': 'der', 'f': 'die', 'n': 'das', 'pl': 'die'
            },
            'accusative': {
                'm': 'den', 'f': 'die', 'n': 'das', 'pl': 'die'
            },
            'dative': {
                'm': 'dem', 'f': 'der', 'n': 'dem', 'pl': 'den'
            },
            'genitive': {
                'm': 'des', 'f': 'der', 'n': 'des', 'pl': 'der'
            }
        }
    }

    # endings for der- and ein- words
    der = {
        'nominative': {
            'm': 'er', 'f': 'e', 'n': 'es', 'pl': 'e'
        },
        'accusative': {
            'm': 'en', 'f': 'e', 'n': 'es', 'pl': 'e'
        },
        'dative': {
            'm': 'em', 'f': 'er', 'n': 'em', 'pl': 'en'
        },
        'genitive': {
            'm': 'es', 'f': 'er', 'n': 'es', 'pl': 'er'
        }
    }

    ein = {
        'nominative': {
            'm': '', 'f': 'e', 'n': '', 'pl': 'e'
        },
        'accusative': {
            'm': 'en', 'f': 'e', 'n': '', 'pl': 'e'
        },
        'dative': {
            'm': 'em', 'f': 'er', 'n': 'em', 'pl': 'en'
        },
        'genitive': {
            'm': 'es', 'f': 'er', 'n': 'es', 'pl': 'er'
        }
    }

    for der_word in ['dies', 'jed', 'jen', 'manch', 'solch', 'welch', 'all']:
        for case in ['nominative', 'accusative', 'dative', 'genitive']:
            for gender in ['m', 'f', 'n', 'pl']:
                if not articles.get(der_word):
                    articles[der_word] = dict()
                if not articles[der_word].get(case):
                    articles[der_word][case] = dict()
                articles[der_word][case][gender] = der_word + der[case][gender]

    for ein_word in ['ein', 'kein', 'dein', 'sein', 'ihr', 'unser', 'eur', 'Ihr']:
        for case in ['nominative', 'accusative', 'dative', 'genitive']:
            for gender in ['m', 'f', 'n', 'pl']:
                if not articles.get(ein_word):
                    articles[ein_word] = dict()
                if not articles[ein_word].get(case):
                    articles[ein_word][case] = dict()
                articles[ein_word][case][gender] = ein_word + ein[case][gender]

    # ein does not have plural case
    for case in ['nominative', 'accusative', 'dative', 'genitive']:
        del articles['ein'][case]['pl']

    # change eur to euer
    articles['euer'] = articles.pop('eur')
    for case in ['nominative', 'accusative', 'dative', 'genitive']:
        for gender in ['m', 'f', 'n', 'pl']:
            if articles['euer'][case][gender] == 'eur':
                articles['euer'][case][gender] = 'euer'

    # write to file
    with open('../data/articles.json', 'w') as js:
        js.write(json.dumps(articles))


if __name__ == '__main__':
    create_articles_json()
