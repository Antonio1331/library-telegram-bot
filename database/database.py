import sqlite3


class Database:
    def __init__(self, db_name: str = "main.db"):
        self.database = db_name

    def execute(self, sql, args=(), commit=False, fetchone=False, fetchall=False):
        with sqlite3.connect(self.database) as db:
            cursor = db.cursor()
            cursor.execute(sql, args)

            res = None
            if fetchone:
                res = cursor.fetchone()
            elif fetchall:
                res = cursor.fetchall()

            if commit:
                db.commit()
        return res

    def create_table_genres(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            genre_name TEXT NOT NULL
        );
        '''
        self.execute(sql, commit=True)

    def create_table_books(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            image TEXT,
            genre_id INTEGER,
            FOREIGN KEY (genre_id) REFERENCES genres(id)
        );
        '''
        self.execute(sql, commit=True)