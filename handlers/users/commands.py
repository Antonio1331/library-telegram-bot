from data.loader import bot, db
from config import ADMINS
from keyboards.default_buttons.default import (
    get_genre_buttons,
    get_admin_commands,
    get_main_menu
)

@bot.message_handler(commands=['start'])
def user_start(message):
    user_id = message.from_user.id
    is_admin = user_id in ADMINS

    main_menu = get_main_menu(is_admin=is_admin)
    bot.send_message(user_id, "Assalomu alaykum! Asosiy menyu:", reply_markup=main_menu)

