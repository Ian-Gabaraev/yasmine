import utilities
import globals
import re
from emotions import smiley


class OnlineDictionary:
    def __init__(self, word, address, soup_ingredients=None):
        self.word = word
        self.address = address
        self.soup_ingredients = soup_ingredients
        self.soup = utilities.cook_soup(self.address)
        self._soup = utilities.cook_soup(globals.SD % self.word)
        if self.soup_ingredients:
            self.all_definitions = [smiley['pushpin'] + definition.text for definition in
                                    self.soup.find_all(
                                        self.soup_ingredients[0],
                                        self.soup_ingredients[1])
                                    ]
        else:
            pass
        self.all_examples = [smiley['speech balloon'] + example.text for example in
                             self._soup.select(
                                     '#all > div', text=True, recursive=True)]

        # To remove indexation (1., 2), (3), etc)
        self.all_examples = list(map(lambda example: re.sub(
            '\(?\d[\)\.]?|\W\(adsbygoogle.*;', '', example), self.all_examples))

    def get_result_as_string(self):
        definitions, examples = utilities.handle_message_size_limit(
            self.all_definitions, self.all_examples)
        result = f"{smiley['green check']}{self.word}" \
                 f"\n{smiley['magnifying glass']} Definitions:" \
                 f"\n{definitions}" \
                 f"\n{smiley['speaker']}Examples:" \
                 f"\n{examples}"
        return result

    def get_all_definitions(self):
        return self.all_definitions

    def get_all_definitions_as_string(self):
        return "\n".join(self.all_definitions)

    def get_all_examples(self):
        return self.all_examples

    def get_common_definition(self):
        return self.all_definitions[0]

    def get_common_example(self):
        return self.all_examples[0]


class WordReference(OnlineDictionary):
    def __init__(self, word):
        self.word = word
        self.address = globals.WR % self.word
        self.soup_ingredients = [
            'span', {'class': 'rh_def'}
        ]
        super().__init__(self.word, self.address, self.soup_ingredients)
        self.all_definitions = [entry
                                for entry in self.all_definitions]
        self.all_definitions = [definition.split(':')[0]
                                for definition in self.all_definitions if definition is not None]


class DictionaryCom(OnlineDictionary):
    def __init__(self, word):
        self.word = word
        self.address = globals.DC % self.word
        super().__init__(self.word, self.address)
        self.div_value = re.compile(r'[1-5]')
        self.all_definitions_raw = self.soup.find_all('div', {'value': self.div_value}, text=True, recursive=True)
        self.all_definitions = [definition.text for definition in self.all_definitions_raw]


class VocabularyCom(OnlineDictionary):
    def __init__(self, word):
        self.word = word
        self.address = globals.VC % self.word
        super().__init__(self.word, self.address)
        self.all_definitions_raw = self.soup.select('div.sense > h3.definition')
        self.all_definitions = [definition.text for definition in self.all_definitions_raw]
        self.all_definitions = [utilities.prettify(definition) for definition in self.all_definitions]


class UrbanDictionary(OnlineDictionary):
    def __init__(self, word):
        self.word = word
        self.address = globals.UD % self.word
        self.soup_ingredients = [
            'div', {'class': 'meaning'}
        ]
        super().__init__(self.word, self.address, self.soup_ingredients)
        self.all_definitions = [entry
                                for entry in self.all_definitions]
        # New bs4 object for examples
        soup = utilities.cook_soup(self.address)
        self.all_examples = soup.find_all('div', {'class': 'example'})
        self.all_examples = [smiley['speech balloon'] + example.text for example in self.all_examples]

    def get_common_example(self):
        return self.all_examples[0].replace("&apos", "'")
