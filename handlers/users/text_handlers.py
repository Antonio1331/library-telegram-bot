from data.loader import bot, db
from config import ADMINS
from telebot.types import Message, CallbackQuery
from keyboards.inline_buttons.inline import get_genres_keyboard, get_books_inline
from keyboards.default_buttons.default import get_admin_commands, get_main_menu


@bot.message_handler(func=lambda message: message.text == "🎁 Janrlar ro‘yxati")
def show_genre_list(message: Message):
    markup = get_genres_keyboard()
    if markup is None:
        bot.send_message(message.chat.id, "📭 Hali hech qanday janr mavjud emas.")
    else:
        bot.send_message(message.chat.id, "📚 Quyidagi janrlardan birini tanlang:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "🛠 Admin buyruqlari")
def show_admin_commands(message: Message):
    if message.from_user.id in ADMINS:
        markup = get_admin_commands()
        bot.send_message(message.chat.id, "Quyidagi buyruqlardan birini tanlang:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "⛔ Bu bo'lim faqat adminlar uchun.")


@bot.callback_query_handler(func=lambda call: call.data.startswith("genre_"))
def genre_selected(call: CallbackQuery):
    genre_id = int(call.data.split("_")[1])
    books = db.execute("SELECT id, title FROM books WHERE genre_id = ?", (genre_id,), fetchall=True)

    if not books:
        bot.answer_callback_query(call.id, "📭 Bu janrda hali kitoblar yo‘q.")
        return

    markup = get_books_inline(books)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📖 Kitoblardan birini tanlang:",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("book_"))
def book_selected(call: CallbackQuery):
    book_id = int(call.data.split("_")[1])
    book = db.execute("SELECT title, description FROM books WHERE id = ?", (book_id,), fetchone=True)

    if not book:
        bot.answer_callback_query(call.id, "❌ Kitob topilmadi.")
        return

    title, description = book
    text = f"📘 *{title}*\n\n📝 {description or 'Izoh mavjud emas.'}"

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

