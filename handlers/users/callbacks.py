from data.loader import bot, db
from telebot.types import CallbackQuery

@bot.callback_query_handler(func=lambda call: call.data.startswith("genre_"))
def handle_genre_callback(call: CallbackQuery):
    genre_id = int(call.data.split("_")[1])

    books = db.execute("SELECT title, description FROM books WHERE genre_id = ?", (genre_id,), fetchall=True)

    if books:
        bot.send_message(call.message.chat.id, f"📚 Tanlangan janrdagi kitoblar:")
        for title, description in books:
            msg = f"<b>{title}</b>\n{description or 'Izoh mavjud emas'}"
            bot.send_message(call.message.chat.id, msg, parse_mode="HTML")
    else:
        bot.send_message(call.message.chat.id, "Bu janrda hali kitoblar mavjud emas.")
