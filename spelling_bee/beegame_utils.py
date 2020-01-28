import sqlite3
import random
import time
import telebot
from spelling_bee.audioengine import *
from spelling_bee.globals import *


token = '1039967013:AAGuA4kvOm2BkJrjv0bwjyzIYGnNOtsSHk4'
bot = telebot.TeleBot(token)


def register_game(hashcode, user_id_1, user_id_2):
    print('REGISTERING GAME...')
    drop_session_table(hashcode)
    create_game_instance(hashcode)
    delete_user_id_from_w2p(user_id_1)
    delete_user_id_from_w2p(user_id_2)
    register_player_in_table_of_opponents(hashcode, user_id_1)
    register_player_in_table_of_opponents(hashcode, user_id_2)
    create_table_of_active_games()
    delete_current_session(user_id_1, user_id_2)
    update_table_of_active_games(user_id_1, hashcode)
    update_table_of_active_games(user_id_2, hashcode)
    spelling_bee(user_id_1, user_id_2, hashcode)


# This is the main function.
# ! Set a timer.
def spelling_bee(user_id_1, user_id_2, game_id):
    print('STARTING GAME...')
    for word in words:
        update_table_of_opponents(game_id, user_id_1, current_word=word)
        update_table_of_opponents(game_id, user_id_2, current_word=word)
        Pronunciation(word).send_voice_message(user_id_1, bot)
        Pronunciation(word).send_voice_message(user_id_2, bot)
        while not both_users_have_answered(game_id):
            time.sleep(1)
        update_table_of_opponents(game_id, user_id_1, answered=0)
        update_table_of_opponents(game_id, user_id_2, answered=0)
    send_scores_to_players(game_id, user_id_1, user_id_2)
    drop_session_table(game_id)
    print('#GAME OVER')


def user_is_playing(user_id):
    print('VALIDATING IF UIP...')
    cursor = sqlite3.connect('active.db')
    sql_command = queries['is_playing'] % user_id
    response = cursor.execute(sql_command)
    result = response.fetchall()
    cursor.close()
    return bool(result)


# Returns a list of 'answered' values
# all(list) returns True if all elements
# of list are equal to 1.
def both_users_have_answered(game_id):
    print('VALIDATING IF BUHA...')
    cursor = sqlite3.connect('active.db')
    sql_command = queries['both_answered'] % game_id
    response = cursor.execute(sql_command)
    result = [status[0] for status in response.fetchall()]
    cursor.close()
    return all(result)


def delete_user_id_from_w2p(user_id):
    print('DELETING USER %r...' % user_id)
    cursor = sqlite3.connect('w2p.db')
    sql_command = queries['delete_from_w2p'] % user_id
    cursor.execute(sql_command)
    cursor.commit()
    cursor.close()


# ! This messages the server, too, fix.
def poll_users(server_id):
    print('POLLING USERS...')
    for user_id in userlist:
        print('NOTIFYING %r...' %user_id)
        bot.send_message(user_id, text=messages['initiative'] % server_id)


def try_to_start_game(message):
    print('ATTEMPTING...')
    player_two = find_player()
    if player_two:
        print('#OPPONENT FOUND')
        return player_two[0]
    else:
        bot.send_message(message.from_user.id, text=messages['lonely'])
        return False


def drop_session_table(game_id):
    print('CLEANING UP...')
    cursor = sqlite3.connect('active.db')
    sql_to_drop_session_table = queries['drop'] % game_id
    try:
        cursor.execute(sql_to_drop_session_table)
        print('#CLEANED UP')
    except sqlite3.OperationalError:
        pass
    finally:
        cursor.close()


def delete_current_session(user_id_1, user_id_2):
    print('DELETING SESSION...')
    cursor = sqlite3.connect('active.db')
    sql_player_one = queries['delete session'] % user_id_1
    sql_player_two = queries['delete session'] % user_id_2
    try:
        cursor.execute(sql_player_one)
        cursor.execute(sql_player_two)
        cursor.commit()
        print('#EXPIRED SESSION REMOVED')
    except sqlite3.OperationalError:
        pass
    finally:
        cursor.close()


def face_control():
    print('LOOKING FOR OPPONENT...')
    cursor = sqlite3.connect('w2p.db')
    sql_command = queries['face_control']
    response = cursor.execute(sql_command)
    result = response.fetchall()
    cursor.close()
    return result


def find_player():
    for _ in range(60):
        if face_control():
            return face_control()[0]
        time.sleep(1)
    return False


def create_game_instance(hashcode):
    print('CREATING GAME INSTANCE...')
    cursor = sqlite3.connect('active.db')
    sql_command = queries['game_instance'].format(table=hashcode)
    cursor.execute(sql_command)
    cursor.commit()
    print('#GAME INSTANCE CREATED')
    cursor.close()


def register_player_in_table_of_opponents(game_id, user_id):
    print('REGISTERING %r in TOOP...' %game_id)
    cursor = sqlite3.connect('active.db')
    sql_command = queries['register'] % (game_id, user_id, 0, 'ZERO', 0, 'ZERO')
    cursor.execute(sql_command)
    cursor.commit()
    print('#PLAYER REGISTERED IN TOOP')
    cursor.close()


# Getters. START.

def get_current_game_id(user_id):
    print('RETRIEVING current game id...')
    cursor = sqlite3.connect('active.db')
    sql_command = queries['current_game'] % user_id
    response = cursor.execute(sql_command)
    return response.fetchone()[0]


def get_current_word(game_id, user_id):
    print('RETRIEVING current word...')
    cursor = sqlite3.connect('active.db')
    sql_command = queries['current_word'] % (game_id, user_id)
    response = cursor.execute(sql_command)
    return response.fetchone()[0]


def get_user_score(game_id, user_id):
    print('RETRIEVING score...')
    cursor = sqlite3.connect('active.db')
    sql_command = queries['current_score'] % (game_id, user_id)
    response = cursor.execute(sql_command)
    return response.fetchone()[0]


def get_current_response(game_id, user_id):
    print('RETRIEVING response...')
    cursor = sqlite3.connect('active.db')
    sql_command = queries['current_response'] % (game_id, user_id)
    response = cursor.execute(sql_command)
    return response.fetchone()[0]

# Getters: END.


def send_scores_to_players(game_id, user_id_1, user_id_2):
    print('>>>SENDING SCORES')
    final_results = dict()
    final_results['first'] = get_user_score(game_id, user_id_1)
    final_results['second'] = get_user_score(game_id, user_id_2)
    print(final_results['first'])
    if final_results['first'] == final_results['second']:
        bot.send_message(user_id_1, text='Draw. Your score is %r' % final_results['first'])
        bot.send_message(user_id_2, text='Draw. Your score is %r' % final_results['second'])
    elif final_results['first'] > final_results['second']:
        bot.send_message(user_id_1, text='You win. Your score is %r' % final_results['first'])
        bot.send_message(user_id_2, text='You lose. Your score is %r' % final_results['second'])
    else:
        bot.send_message(user_id_2, text='You win. Your score is %r' % final_results['second'])
        bot.send_message(user_id_1, text='You lose. Your score is %r' % final_results['first'])


def answer_is_correct(game_id, user_id):
    print('VALIDATING...')
    return get_current_word(game_id, user_id) == get_current_response(game_id, user_id)


def create_table_of_active_games():
    print('CREATING TOAG...')
    cursor = sqlite3.connect('active.db')
    sql_command = queries['create_active_games']
    cursor.execute(sql_command)
    cursor.commit()
    cursor.close()


def update_table_of_opponents(game_id, user_id, **kwargs):
    print("UPDATING TOOP %r..." % game_id)
    cursor = sqlite3.connect('active.db')
    sql_command = queries['update_opponents'] \
                %(game_id, list(kwargs.keys())[0], list(kwargs.values())[0], user_id)
    cursor.execute(sql_command)
    cursor.commit()
    cursor.close()


def update_table_of_active_games(user_id, game_id):
    print("UPDATING TOAG %r..." % game_id)
    cursor = sqlite3.connect('active.db')
    sql_command = queries['update_active_games'] % (game_id, user_id)
    cursor.execute(sql_command)
    cursor.commit()
    cursor.close()


def create_table_of_w2p():
    print('CREATING W2P...')
    cursor = sqlite3.connect('w2p.db')
    sql_command = queries['create_w2p']
    cursor.execute(sql_command)
    cursor.commit()
    cursor.close()


def add_player_id_to_w2p(user_id, is_creator):
    print('ADDING PLAYER 2 W2P %r...' %user_id)
    create_table_of_w2p()
    cursor = sqlite3.connect('w2p.db')
    sql_command = queries['add_user'] % (user_id, is_creator)
    cursor.execute(sql_command)
    cursor.commit()
    cursor.close()


# Hashcode is characters only.
# SQLite dislikes alphanumerical column names.
def generate_hashcode():
    print('GENERATING HASHCODE...')
    characters = [chr(i) for i in range(97, 122)]
    hashcode = str()
    for _ in range(4):
        hashcode += characters[random.randint(0, len(characters)-1)]
    return hashcode


def increment_user_score(current_game_id, user_id):
    print('INCREMENT USER SCORE...')
    current_user_score = get_user_score(current_game_id, user_id)
    update_table_of_opponents(current_game_id, user_id, score=current_user_score+1)


def check_answer(message):
    print('VALIDATING...')
    current_game_id = get_current_game_id(message.from_user.id)
    update_table_of_opponents(current_game_id, message.from_user.id, answered=1)
    update_table_of_opponents(current_game_id, message.from_user.id, response=message.text.lower())
    if answer_is_correct(current_game_id, message.from_user.id):
        bot.send_message(message.from_user.id, text='Correct!')
        increment_user_score(current_game_id, message.from_user.id)
    else:
        bot.send_message(message.from_user.id, text='Wrong!')


@bot.message_handler(regexp='^[a-zA-Z]+')
def intercept(message):
    print('>>>INPUT INTERCEPTED<<<')
    if user_is_playing(message.from_user.id):
        check_answer(message)
