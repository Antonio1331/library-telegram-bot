from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu(is_admin=False):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if is_admin:
        markup.add(KeyboardButton("🛠 Admin buyruqlari"))
    markup.add(KeyboardButton("🎁 Janrlar ro‘yxati"))
    return markup


def get_admin_commands():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton("➕ Janr qo'shish"),
        KeyboardButton("📚 Kitob qo'shish")
    )
    markup.row(
        KeyboardButton("🗑 Kitob o'chirish"),
        KeyboardButton("⬅️ Ortga")
    )
    return markup


def get_genre_buttons(genres):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for _, name in genres:
        markup.add(KeyboardButton(name))
    return markup
