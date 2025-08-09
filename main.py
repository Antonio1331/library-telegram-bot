from data.loader import bot, db
from handlers.users import text_handlers
import handlers.users.commands
import handlers.users.callbacks
import handlers.admins.text_handlers
import handlers.admins.commands
import handlers.admins.callbacks


if __name__ == '__main__':
    db.create_table_genres()
    db.create_table_books()
    bot.infinity_polling()
