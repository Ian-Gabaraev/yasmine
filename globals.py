# Global settings for Yasmine Project

import telebot
import re
from emotions import smiley

TOKEN = None
bot = telebot.TeleBot(TOKEN)


# Links to websites to grab data from.
HJ = 'https://howjsay.com/mp3/%s.mp3'
WR = 'https://www.wordreference.com/definition/%s'
DC = 'https://www.dictionary.com/browse/%s?s=t'
SD = 'https://sentencedict.com/%s.html'
VC = 'https://www.vocabulary.com/dictionary/%s'
UD = 'https://www.urbandictionary.com/define.php?term=%s'


# Change these when code is migrating to new host.
path_to_pronunciation = 'audio/pronunciation/'
path_to_podcasts = 'audio/temp/'
path_to_images = 'images/'
path_to_user_dictionaries = 'dictionaries/vocabulary.db'
path_to_presets = 'dictionaries/presets.db'


# Absolute paths to folders containing mp4 videos.
# Used as attachments to bot's messages.
paths_to_GIF = {
    'wrong': '/Users/ian/PycharmProjects/yasmine/images/wrong',
    'correct': '/Users/ian/PycharmProjects/yasmine/images/correct',
    'meaning': '/Users/ian/PycharmProjects/yasmine/images/meaning',
    'error': '/Users/ian/PycharmProjects/yasmine/images/error',
    'win': '/Users/ian/PycharmProjects/yasmine/images/win',
    'lose': '/Users/ian/PycharmProjects/yasmine/images/correct',
    'hello': '/Users/ian/PycharmProjects/yasmine/images/hello',
    'crypto': '/Users/ian/PycharmProjects/yasmine/images/crypto',
}


# !TEMPORARY.
words = ['irk', 'tick', 'sick', 'meek']


# Add/Remove, used by crypto.py
favorite_crypto_pairs = [
    'BTC/USD',
    'BTC/ETH',
    'BTC/LTC',
    'USD/RUR',
    'EUR/RUR',
]


wrong_characters = [
            f"{smiley['pushpin']}\n",
            f"{smiley['pushpin']}\t",
            f"{smiley['pushpin']}.",
            f"{smiley['pushpin']} ",
            f"{smiley['pushpin']} \n",
            f"{smiley['pushpin']}",
            f"{smiley['books']}\n",
            f"{smiley['books']}\t",
            f"{smiley['books']}.",
            f"{smiley['books']} ",
            f"{smiley['books']} \n",
            f"{smiley['books']}",
            '\n'
]


# Links to radio stations.
podcast_sources = [

]


# Links and regex's for /read
# Format: website address: hyperlink pattern of articles
favorite_websites = {
    'sport': {
        'http://nerdfitness.com':
            ('a', {'href': re.compile(r'https://.*/blog/')}),
    },
    'health': {
        'http://verywellmind.com':
            ('a', {'class': 'block-small'}),
    },
    'gaming': {
        'https://www.thatvideogameblog.com/':
            ('a', {'href': re.compile(r'https://.*/20\d{2}/.*')}),
        'https://www.vg247.com/':
            ('a', {'href': re.compile(r'https://.*/20\d{2}/.*')}),
    },
    'languages': {},
    'psychology': {
        'http://spring.org.uk':
            ('a', {'href': re.compile(r'https://.*/20\d{2}/')}),
    },
    'travel': {
        'http://nomadicmatt.com/travel-blog/':
            ('a', {'class': 'entry-title-link'}),
    },
    'art': {
        'http://www.booooooom.com/':
            ('a', {'href': re.compile(r'https://.*/20\d{2}/.*')}),
    },
    'books': {
        'http://johnpistelli.com':
            ('a', {'href': re.compile(r'https://.*/20\d{2}.*')}),
    },
    'comedy': {
        'http://thehardtimes.net':
            ('a', {'href': re.compile(r'https://.*\/(music|culture|blog)\/(?:.+-){3,}')})
    },
    'news': {
        'http://nypost.com/video/':
            ('a', {'href': re.compile(r'https://.*\/video\/(?:.*-)+')}),
    }
}


sql_queries = {
            'everything':
                'SELECT * FROM %r',
            'everything ordered':
                'SELECT word, definition, example FROM %r ORDER BY word, definition, example',
            'words':
                'SELECT DISTINCT word FROM %r',
            'definitions':
                'SELECT DISTINCT definition FROM %r',
            'examples':
                'SELECT DISTINCT example FROM %r',
            'words ordered':
                'SELECT DISTINCT word FROM %r ORDER BY word',
            'definitions ordered':
                'SELECT DISTINCT definition FROM %r ORDER BY definition',
            'examples ordered':
                'SELECT DISTINCT example FROM %r ORDER BY example',
            'number of words':
                'SELECT count(word) FROM %r',
            'delete row':
                'DELETE FROM %r WHERE word = %r',
            'exists':
                'SELECT EXISTS(SELECT * FROM %r WHERE word = %r)',
            'add entry':
                'INSERT INTO %r VALUES(%r, %r, %r, %r)',
}
