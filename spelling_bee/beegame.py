from spelling_bee.beegame_utils import *


@bot.message_handler(commands=['holler'])
def holler(message):
    add_player_id_to_w2p(message.from_user.id, 1)
    poll_users(message.from_user.id)
    second_player = try_to_start_game(message)
    if second_player:
        hashcode = generate_hashcode()
        register_game(hashcode, message.from_user.id, second_player)
    else:
        pass


@bot.message_handler(commands=['join'])
def join(message):
    add_player_id_to_w2p(message.from_user.id, 0)


bot.polling()
