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

    def get_calorie(self, user_id):
        user_id_int = int(re.sub(r"\D", "", user_id.strip()))
        results = self.db.get_items(user_id = user_id_int)
        return [{'date': item[0], 'calorie': item[1]} for item in results]

    def __del__(self):
        self.db.close()
