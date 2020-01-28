import crawlers
from globals import *


class Find:
    def __init__(self, word):
        self.word = word
        self.definitions = None
        self.examples = None

    def load_definitions(self):
        objects = [
            crawlers.WordReference(self.word),
            crawlers.VocabularyCom(self.word),
            crawlers.DictionaryCom(self.word)
        ]

        for obj in objects:
            if not self.definitions:
                self.definitions = list(set([definition for definition in
                                        obj.get_all_definitions()
                                        if definition not in wrong_characters]))
            else:
                break

    def load_examples(self):
        self.examples = crawlers.WordReference(self.word).get_all_examples()

    def get_all_definitions(self):
        try:
            self.load_definitions()
        except TypeError:
            print('Definitions did not load.')
        else:
            return self.definitions

    def get_all_definitions_as_string(self):
        try:
            self.load_definitions()
        except TypeError:
            print('Definitions did not load.')
        else:
            return "\n".join(self.definitions)

    def get_all_examples(self):
        try:
            self.load_examples()
        except TypeError:
            print('Examples did not load.')
        else:
            return self.examples

    def get_result_as_string(self):
        definitions = '\n'.join(self.get_all_definitions())
        examples = '\n'.join(self.get_all_examples())
        result = f"{smiley['green check']}{self.word}" \
                 f"\n{smiley['magnifying glass']} Definitions:" \
                 f"\n{definitions}" \
                 f"\n{smiley['speaker']}Examples:" \
                 f"\n{examples}"
        return result

    def get_common_definition(self):
        try:
            self.load_definitions()
            return self.definitions[0]
        except TypeError:
            return "Definitions did not load."
        except IndexError:
            return "Nothing found."

    def get_common_example(self):
        try:
            self.load_examples()
            for example in self.examples:
                yield example
        except TypeError:
            return "Examples did not load."
        except IndexError:
            return "Nothing found."

    def get_results_in_brief(self):
        if len(self.examples) > 5:
            self.examples = [self.get_common_example() for _ in range(5)]
        return self.get_result_as_string()
