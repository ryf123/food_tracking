import sqlite3

class SQLiteDB:
    TABLE_NAME = 'food_consumed'

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        if(not self.table_exists(self.TABLE_NAME)):
            self.create_table()
    
    def table_exists(self, table_name):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        return self.cursor.fetchone() is not None
    
    def create_table(self):
        self.cursor.execute(f'''
            CREATE TABLE {self.TABLE_NAME} (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                transcribed_text TEXT,
                translated_text TEXT,
                calories INTEGER,
                food_table BLOB,
                timestamp REAL,
                date TEXT,
                time TEXT
            )
        ''')
        self.conn.commit()

    def insert(self, user_id, transcribed_text, translated_text, calories, food_table, timestamp, date, time):
        self.cursor.execute(f"INSERT INTO {self.TABLE_NAME} (user_id, transcribed_text, translated_text, calories, food_table, timestamp, date, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (user_id, transcribed_text, translated_text, calories, food_table, timestamp, date, time))
        self.conn.commit()

    def get_items(self, user_id):
        query = f"SELECT date, sum(calories) FROM {self.TABLE_NAME} where user_id = {user_id} group by date order by date DESC"
        print(query)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()