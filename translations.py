import utilities
from emotions import smiley


class Translate:
    def __init__(self, link):
        self.soup = utilities.cook_soup(link)
        self.common = [smiley['green check'] + entry.text for entry in self.soup.find_all(
            'a', {'class': 'dictLink featured'})]

    def translate(self):
        return '\n'.join(self.common)


class EnIt(Translate):
    def __init__(self, word):
        self.link = f'https://www.linguee.com/english-italian/translation/{word}.html'
        super().__init__(self.link)


class RuEn(Translate):
    def __init__(self, word):
        self.link = f'https://www.linguee.com/russian-english/translation/{word}.html'
        super().__init__(self.link)


class EnFr(Translate):
    def __init__(self, word):
        self.link = f'https://linguee.com/english-french/search?query={word}'
        super().__init__(self.link)


class EnRu(Translate):
    def __init__(self, word):
        self.link = f'https://www.linguee.com/english-russian/search?query={word}'
        super().__init__(self.link)


class EnDe(Translate):
    def __init__(self, word):
        self.link = f'https://www.linguee.com/english-german/translation/{word}.html'
        super().__init__(self.link)
