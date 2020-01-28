import utilities
import crawlers
import crypto
import translations
from default_messages import result_messages
from genius import Find
from globals import *
from emotions import smiley
from keyboards import articles_categories


@bot.message_handler(commands=['start'])
def start(message):
    utilities.greet_user(message)
    utilities.register_user(message)
    utilities.create_user_dictionary(message)
    utilities.send_manual_to_user(message)


@bot.message_handler(commands=['truncate'])
def truncate(message):
    utilities.truncate_user_table(message)


@bot.message_handler(commands=['ud'])
def find_in_urban_dictionary(message):
    word = utilities.extract_arg(message.text)
    result = crawlers.UrbanDictionary(word).get_result_as_string()
    utilities.send_animated_message(message, result, category='meaning')


# This is slow :(
@bot.message_handler(commands=['d', 'define'])
def get_full_info_on_word(message):
    word = utilities.extract_arg(message.text)
    result = Find(word).get_result_as_string()
    utilities.send_animated_message(message, result, category='meaning')


# Using WordReference for better speed
@bot.message_handler(commands=['m', 'means', 'wr'])
def define_a_word(message):
    word = utilities.extract_arg(message.text)
    result = crawlers.WordReference(word).get_all_definitions_as_string()
    utilities.send_animated_message(message, result, 'meaning')


def send_random_article_to_user(message, category):
    link_to_random_article = utilities.pick_an_article(category)
    bot.send_message(message.from_user.id, link_to_random_article)


@bot.message_handler(commands=['say'])
def find_pronunciation(message):
    word = utilities.extract_arg(message.text)
    try:
        result = utilities.grab_pronunciation(word)
    except FileNotFoundError:
        utilities.send_animated_message(message, result_messages['wrong word'], 'error')
    else:
        bot.send_voice(message.from_user.id, result)


# ! DUPLICATE CODE.
def find_and_send_pronunciation(message, word):
    try:
        result = utilities.grab_pronunciation(word)
    except FileNotFoundError:
        utilities.send_animated_message(message, result_messages['wrong word'], 'wrong')
    else:
        bot.send_voice(message.from_user.id, result)


@bot.message_handler(commands=['enit'])
def english_to_italian(message):
    word = utilities.extract_arg(message.text)
    result = translations.EnIt(word).translate()
    utilities.send_animated_message(message, result, category='meaning')


@bot.message_handler(commands=['enfr'])
def english_to_french(message):
    word = utilities.extract_arg(message.text)
    result = translations.EnFr(word).translate()
    utilities.send_animated_message(message, result, category='meaning')


@bot.message_handler(commands=['enru'])
def english_to_russian(message):
    word = utilities.extract_arg(message.text)
    result = translations.EnRu(word).translate()
    utilities.send_animated_message(message, result, category='meaning')


@bot.message_handler(commands=['ruen'])
def russian_to_english(message):
    word = utilities.extract_arg(message.text)
    result = translations.RuEn(word).translate()
    utilities.send_animated_message(message, result, category='meaning')


@bot.message_handler(commands=['ende'])
def english_to_german(message):
    word = utilities.extract_arg(message.text)
    result = translations.EnDe(word).translate()
    utilities.send_animated_message(message, result, category='meaning')


@bot.message_handler(commands=['crypto', 'c'])
def crypto_stats(message):
    utilities.send_animated_message(message, crypto.check_favorites(), category='crypto')


@bot.message_handler(commands=['wh', 'whoami'])
def who_am_i(message):
    bot.reply_to(message, str(utilities.get_user_credentials(message)))


# Develop a database for podcasts, updates in the morning.
@bot.message_handler(commands=['pod', 'podcast'])
def get_random_podcast(message):
    pass


@bot.message_handler(commands=['s', 'see'])
def see_user_dictionary(message):
    bot.reply_to(message, utilities.list_all_words_of_user_as_string(message))


@bot.message_handler(commands=['r', 'random'])
def get_random_word_from_table(message):
    entry = utilities.get_random_word_from_table("data/presets.db", "devilish")
    result = f"{smiley['pushpin']}{entry[0]}\n" \
             f"{smiley['books']}{entry[1]}\n" \
             f"{smiley['speech balloon']}{entry[2]}"
    utilities.send_animated_message(message, result, category='meaning')
    find_and_send_pronunciation(message, entry[0])


@bot.message_handler(commands=['a', 'add'])
def add_word_to_user_dictionary(message):
    word = utilities.extract_arg(message.text)
    response = Find(word)
    utilities.add_word_to_vocabulary(message, word, response.get_common_definition(),
                                     response.get_common_example())
    bot.reply_to(message, result_messages['ready'])


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    send_random_article_to_user(call, call.data)


@bot.message_handler(commands=['read', 'reading'])
def post_random_article(message):
    bot.send_message(message.from_user.id, 'Which category?', reply_markup=articles_categories)
    # apihelper.edit_message_text(TOKEN, chat_id=call.chat.id, message_id=call.message_id, text='Hello')


bot.polling()
