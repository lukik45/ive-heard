import sqlite3 as sl
from __config import DATABASE_PATH
from word import Word

class DataAccessObject:
    def __init__(self):
        self.connection = sl.connect(DATABASE_PATH)

    def __del__(self):
        self.connection.close()

    def create_words_table(self):
        with self.connection:
            self.connection.execute(f"""CREATE TABLE WORDS (
                                    id INTEGER PRIMARY KEY, 
                                    word TEXT,
                                    status INTEGER);""")
            
    def insert_word(self, word:Word):
        with self.connection:
            self.connection.execute(f"INSERT INTO WORDS (word, status) VALUES ('{word.text}', {word.status});")

    def update_word(self, word:Word):
        with self.connection:
            self.connection.execute(f"UPDATE WORDS SET status = {word.status} WHERE id = {word.id};")
    
    def delete_word(self, word:Word):
        with self.connection:
            self.connection.execute(f"DELETE FROM WORDS WHERE id = {word.id};")

    def get_words(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM WORDS;").fetchall()
        

if __name__ == "__main__":
    dao = DataAccessObject()
    # dao.create_words_table()
    # dao.insert_word(Word("hello", 1,1))
    # dao.insert_word(Word("world", 0,0))
    print(dao.get_words())