# 📚 Library Telegram Bot

**Library Telegram Bot** — bu Telegram orqali ishlaydigan kutubxona tizimi bo‘lib, foydalanuvchilarga janr va kitoblar bo‘yicha qulay qidiruv imkoniyatini beradi. Ma’lumotlar **SQLite** bazasida saqlanadi.

## 🔹 Xususiyatlari
- **Admin imkoniyatlari**:
  - Yangi janr qo‘shish
  - Yangi kitob qo‘shish (nomi, tavsifi, janri bilan)
  - Kitobni o‘chirish
- **Foydalanuvchilar uchun**:
  - Janrlar ro‘yxatini ko‘rish
  - Tanlangan janrdagi kitoblar ro‘yxatini ko‘rish
  - Kitobning nomi va tavsifi (kitob nima haqida) bilan tanishish

## 🛠 Texnologiyalar
- Python
- [pyTelegramBotAPI (Telebot)](https://pypi.org/project/pyTelegramBotAPI/)
- SQLite

## 📌 Qisqacha ishlash jarayoni
1. **Admin** panel orqali yangi janrlar va kitoblar qo‘shadi yoki o‘chiradi.
2. **Foydalanuvchi** bot orqali janr tanlaydi.
3. Tanlangan janrdagi kitoblar ro‘yxati chiqadi.
4. Kitob ustiga bosilganda, uning nomi va tavsifi ko‘rsatiladi.

