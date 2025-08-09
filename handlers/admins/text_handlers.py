from data.loader import bot, db
from keyboards.default_buttons import default
from keyboards.default_buttons.default import get_genre_buttons
from config import ADMINS
from telebot.types import Message

kitob_qoshish_data = {}


@bot.message_handler(func=lambda m: m.text == "➕ Janr qo'shish" and m.from_user.id in ADMINS)
def ask_genre_name(message):
    msg = bot.send_message(message.chat.id, "📚 Yangi janr nomini kiriting:")
    bot.register_next_step_handler(msg, save_genre)

def save_genre(message):
    genre_name = message.text.strip()
    db.execute("INSERT INTO genres (genre_name) VALUES (?)", (genre_name,), commit=True)
    bot.send_message(
        message.chat.id,
        f"✅ Janr '{genre_name}' muvaffaqiyatli qo‘shildi!",
        reply_markup=default.get_admin_commands()
    )


@bot.message_handler(func=lambda m: m.text == "📚 Kitob qo'shish" and m.from_user.id in ADMINS)
def ask_book_title(message: Message):
    user_id = message.from_user.id
    kitob_qoshish_data[user_id] = {}
    msg = bot.send_message(message.chat.id, "📖 Kitob sarlavhasini kiriting:")
    bot.register_next_step_handler(msg, ask_book_genre)

def ask_book_genre(message: Message):
    user_id = message.from_user.id
    kitob_qoshish_data[user_id]['title'] = message.text.strip()

    genres = db.execute("SELECT id, genre_name FROM genres", fetchall=True)
    if not genres:
        bot.send_message(message.chat.id, "❌ Avval janr qo‘shing.")
        return

    markup = get_genre_buttons(genres)  # default keyboard bo'lishi kerak
    msg = bot.send_message(message.chat.id, "📚 Janrni tanlang:", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_book_description)

def ask_book_description(message: Message):
    user_id = message.from_user.id
    kitob_qoshish_data[user_id]['genre_name'] = message.text.strip()

    msg = bot.send_message(message.chat.id, "✍️ Kitob haqida qisqacha izoh kiriting:", reply_markup=None)
    bot.register_next_step_handler(msg, save_book)

def save_book(message: Message):
    user_id = message.from_user.id
    kitob_qoshish_data[user_id]['description'] = message.text.strip()
    data = kitob_qoshish_data[user_id]

    genre = db.execute("SELECT id FROM genres WHERE genre_name = ?", (data['genre_name'],), fetchone=True)
    if genre:
        genre_id = genre[0]
        db.execute(
            "INSERT INTO books (title, description, genre_id) VALUES (?, ?, ?)",
            (data['title'], data['description'], genre_id),
            commit=True
        )
        bot.send_message(
            message.chat.id,
            f"✅ Kitob '{data['title']}' muvaffaqiyatli qo‘shildi!",
            reply_markup=default.get_admin_commands()
        )
    else:
        bot.send_message(
            message.chat.id,
            "❌ Bunday janr topilmadi. Avval uni qo‘shing.",
            reply_markup=default.get_admin_commands()
        )

    kitob_qoshish_data.pop(user_id, None)


@bot.message_handler(func=lambda m: m.text == "🗑 Kitob o'chirish" and m.from_user.id in ADMINS)
def ask_book_to_delete(message):
    books = db.execute("SELECT id, title FROM books", fetchall=True)
    if not books:
        bot.send_message(message.chat.id, "📭 Hech qanday kitob topilmadi.")
        return

    text = "O'chirmoqchi bo‘lgan kitob raqamini tanlang:\n"
    for i, (bid, title) in enumerate(books, 1):
        text += f"{i}. {title}\n"

    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler_by_chat_id(message.chat.id, lambda msg: delete_book(msg, books))

def delete_book(message, books):
    try:
        index = int(message.text) - 1
        book_id = books[index][0]
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri tanlov. Qayta urinib ko‘ring.")
        return

    db.execute("DELETE FROM books WHERE id = ?", (book_id,), commit=True)
    bot.send_message(message.chat.id, "✅ Kitob muvaffaqiyatli o‘chirildi.", reply_markup=default.get_admin_commands())

@bot.message_handler(func=lambda m: m.text == "⬅️ Ortga")
def go_back(message):
    bot.send_message(
        message.chat.id,
        "🔙 Ortga qaytdingiz.",
        reply_markup=default.get_main_menu(is_admin=message.from_user.id in ADMINS)
    )
