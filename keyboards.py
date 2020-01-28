from telebot import types
from emotions import smiley

articles_categories = types.InlineKeyboardMarkup(row_width=2)

articles_categories.add(types.InlineKeyboardButton(f"{smiley['palette']} Art", callback_data='art'),
                        types.InlineKeyboardButton(f"{smiley['brain']} Psychology", callback_data='psychology'))


articles_categories.add(types.InlineKeyboardButton(f"{smiley['joystick']} Gaming", callback_data='gaming'),
                        types.InlineKeyboardButton(f"{smiley['books']} Books", callback_data='books'))


articles_categories.add(types.InlineKeyboardButton(f"{smiley['newspaper']} News", callback_data='news'),
                        types.InlineKeyboardButton(f"{smiley['airplane']} Travel", callback_data='travel'))


articles_categories.add(types.InlineKeyboardButton(f"{smiley['clown']} Comedy", callback_data='news'),
                        types.InlineKeyboardButton(f"{smiley['pill']} Health", callback_data='travel'))


articles_categories.add(types.InlineKeyboardButton(f"{smiley['runner']} Sport", callback_data='sport'),
                        types.InlineKeyboardButton(f"{smiley['usa']} Languages", callback_data='languages'))


articles_categories.add(types.InlineKeyboardButton(f"{smiley['question mark']} Any", callback_data='any'))
