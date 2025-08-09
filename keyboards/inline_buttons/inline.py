from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.loader import db

def get_delete_books_keyboard():
    books = db.execute("SELECT id, title FROM books", fetchall=True)

    if not books:
        return None

    markup = InlineKeyboardMarkup()
    for book_id, title in books:
        markup.add(InlineKeyboardButton(text=title, callback_data=f"deletebook_{book_id}"))

    return markup


def get_genres_keyboard():
    genres = db.execute("SELECT id, genre_name FROM genres", fetchall=True)
    if not genres:
        return None

    markup = InlineKeyboardMarkup()
    for genre_id, genre_name in genres:
        markup.add(InlineKeyboardButton(text=genre_name, callback_data=f"genre_{genre_id}"))
    return markup

def get_books_inline(books):
    markup = InlineKeyboardMarkup()
    for book_id, title in books:
        markup.add(InlineKeyboardButton(text=title, callback_data=f"book_{book_id}"))
    return markup
