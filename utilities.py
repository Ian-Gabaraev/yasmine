import requests
import sqlite3
import emotions
import random
import os
import time
import default_messages
from emotions import smiley
from bs4 import BeautifulSoup
from requests.exceptions import MissingSchema, ConnectionError
from globals import bot
from globals import paths_to_GIF
from globals import HJ, path_to_pronunciation, favorite_websites
from large_texts import *


def extract_arg(arg):
    return ' '.join(arg.split()[1:])


def create_users_database():
    command = """
    CREATE TABLE users
    (uid INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    nickname TEXT,
    joined NUMERIC,
    UNIQUE(uid)
    );
    """
    connection = sqlite3.connect('data/primary.db')
    cursor = connection.cursor()
    cursor.execute(command)
    connection.commit()
    connection.close()


def create_user_dictionary(message):
    nickname = get_user_credentials(message)['nickname']
    command = """
    CREATE TABLE IF NOT EXISTS %r
    (word TEXT PRIMARY KEY,
    definition TEXT,
    example TEXT,
    UNIQUE(word)
    );
    """ % nickname
    connection = sqlite3.connect('dictionaries/vocabulary.db')
    cursor = connection.cursor()
    cursor.execute(command)
    connection.commit()
    connection.close()


def create_custom_vocabulary_table(database, table_name):
    command = "CREATE TABLE IF NOT EXISTS %s" \
              "(word TEXT PRIMARY KEY," \
              "definition TEXT," \
              "example TEXT," \
              "exposed INTEGER,"\
              "guessed INTEGER,"\
              "rating INTEGER,"\
              "UNIQUE(word));"
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute(command % table_name)
    connection.commit()
    connection.close()


def list_all_words_from_table(database, table_name):
    # connection = sqlite3.connect("data/presets.db")
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    sql_command = "SELECT word, definition, example FROM %r ORDER BY word ASC" % table_name
    cursor.execute(sql_command)
    result = cursor.fetchall()
    connection.close()
    return result


def get_random_word_from_table(database, table_name):
    entries = list_all_words_from_table(database, table_name)
    random_integer = random.randint(0, len(entries)-1)
    return entries[random_integer]


def populate_custom_vocabulary_table(database, table_name, word, definition, example):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO %r"
                    "VALUES(%r, %r, %r);" % (table_name, word, definition, example))
    connection.commit()
    connection.close()


def update_users_database(uid, first_name, last_name, nickname, joined):
    print(uid, first_name, last_name, nickname, joined)
    connection = sqlite3.connect('data/primary.db')
    cursor = connection.cursor()
    command = "INSERT OR IGNORE INTO users  VALUES(%d, %r, %r, %r, %r)" \
              % (uid, first_name, last_name, nickname, joined)
    cursor.execute(command)
    connection.commit()
    connection.close()


def truncate_user_table(message):
    nickname = get_user_credentials(message)['nickname']
    connection = sqlite3.connect('dictionaries/vocabulary.db')
    cursor = connection.cursor()
    command = "TRUNCATE TABLE %r;" % nickname
    cursor.execute(command)
    connection.commit()
    connection.close()


def list_all_users_by_uid():
    connection = sqlite3.connect('data/primary.db')
    cursor = connection.cursor()
    sql_command = 'SELECT uid FROM users'
    cursor.execute(sql_command)
    result = cursor.fetchall()
    connection.close()
    return result


def list_all_words_of_user(message):
    nickname = get_user_credentials(message)['nickname']
    connection = sqlite3.connect("dictionaries/vocabulary.db")
    cursor = connection.cursor()
    sql_command = "SELECT word FROM %r ORDER BY word ASC" % nickname
    cursor.execute(sql_command)
    result = cursor.fetchall()
    result = [smiley['pushpin'] + word[0] for word in result]
    connection.close()
    return result


def list_all_words_of_user_as_string(message):
    if list_all_words_of_user(message):
        return "\n".join(list_all_words_of_user(message))
    else:
        return default_messages.error_messages['nf']


def add_word_to_vocabulary(message, word, definition, example):
    nickname = get_user_credentials(message)['nickname']
    connection = sqlite3.connect("dictionaries/vocabulary.db")
    cursor = connection.cursor()
    command = "INSERT OR IGNORE INTO %r VALUES (%r, %r, %r)" % (nickname, word, definition, example)
    cursor.execute(command)
    connection.commit()
    connection.close()


def get_user_credentials(message):
    credentials = dict()
    credentials['uid'] = message.from_user.id
    if not message.from_user.first_name:
        credentials['first_name'] = 'Freaking'
    else:
        credentials['first_name'] = message.from_user.first_name
    if not message.from_user.last_name:
        credentials['last_name'] = 'Mysterious'
    else:
        credentials['last_name'] = message.from_user.last_name
    if not message.from_user.username:
        credentials['nickname'] = str(message.from_user.id)
    else:
        credentials['nickname'] = message.from_user.username
    credentials['language'] = message.from_user.language_code
    return credentials


def greet_user(message):
    random_number = random.randint(0, len(emotions.salutations)-1)
    greeting = emotions.salutations[random_number]
    uid = get_user_credentials(message)['uid']
    first_name = get_user_credentials(message)['first_name']
    last_name = get_user_credentials(message)['last_name']
    text = f"{greeting} {first_name} {last_name}."
    bot.send_message(uid, text=text)


def register_user(message):
    joined = time.strftime('%Y-%m-%d')
    credentials = get_user_credentials(message)
    update_users_database(credentials['uid'],
                                    credentials['first_name'],
                                    credentials['last_name'],
                                    credentials['nickname'],
                                    joined
                                    )


def send_manual_to_user(message):
    uid = get_user_credentials(message)['uid']
    bot.send_message(uid, text=manual)


def cook_soup(link):
    try:
        response = requests.get(link)
    except ConnectionError as ce:
        print('Wrong link %s. Exception message: %s' % (link, str(ce)))
    except MissingSchema as ms:
        print('Wrong link %s. Exception message: %s' % (link, str(ms)))
    else:
        # source = response.text.encode('utf-8').decode('ascii', 'ignore')
        source = response.content
        soup = BeautifulSoup(source, features='html.parser')
        return soup


def attach_video(message, category):
    list_of_GIFs = os.listdir(paths_to_GIF[category])
    random_integer = random.randint(0, len(list_of_GIFs)-1)
    filename = list_of_GIFs[random_integer]
    video = open('%s/%s' %(paths_to_GIF[category], filename), 'rb')
    bot.send_video(message.from_user.id, video)


def prettify(definition):
    string = ""
    definition = definition.split(' ')
    del definition[0]
    for i in definition:
        if i not in ['', '\r\n\t\t\t\t\t\t', '\t', '\n']:
            string += "%s " % i
    return string.rstrip()


def send_animated_message(message, message_text, category):
    attach_video(message, category)
    bot.send_message(message.from_user.id, message_text)


def grab_pronunciation(word):
    response = requests.get(HJ % word)
    if not word or response.status_code != 200:
        raise FileNotFoundError
    else:
        with open('%s%s.mp3' % (path_to_pronunciation, word), 'wb') as audio_file:
            audio_file.write(response.content)
        audio = open('%s%s.mp3' % (path_to_pronunciation, word), 'rb')
        return audio


def handle_message_size_limit(definitions, examples):
    while(len('\n'.join(definitions) + '\n'.join(examples))) >= 4096:
        try:
            definitions.pop()
            examples.pop()
        except IndexError:
            pass
    return ['\n'.join(definitions), '\n'.join(examples)]


def pick_an_article(category):
    random_integer = random.randint(0, len(favorite_websites[category]) - 1)
    random_website_link = list(favorite_websites[category].keys())[random_integer]
    soup = cook_soup(random_website_link)
    html_attributes = favorite_websites[category][random_website_link]
    # set() To rule out repeating links
    set_of_links = set()
    for random_website_link in soup.find_all(html_attributes[0], html_attributes[1]):
        set_of_links.add(random_website_link['href'])
    random_article_index = random.randint(0, len(set_of_links)-1)
    return list(set_of_links)[random_article_index]
