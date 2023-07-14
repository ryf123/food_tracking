from sqlite_db import SQLiteDB
import ast
import datetime
import re

class DBAccess:
    def __init__(self):
        self.db = SQLiteDB('mydatabase.db')

    def insert_to_db(self, user_id, results):
        for result in results:
            self.db.insert(
                user_id = user_id,
                transcribed_text = result['text'],
                translated_text = '',
                calories = result['total_calorie'],
                food_table = '',
                timestamp = datetime.datetime.utcnow().timestamp(),
                date = str(datetime.date.today()),
                time = str(datetime.datetime.now().time()))


    def __del__(self):
        self.db.close()