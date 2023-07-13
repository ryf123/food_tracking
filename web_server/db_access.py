from sqlite_db import SQLiteDB
import ast
import datetime
import re

class DBAccess:
    def __init__(self):
        self.db = SQLiteDB('mydatabase.db')

    def insert_to_db(self, user_id, preprocessed_text):
        # Perform transcription using OpenAI Whisper API
        result = self.process_transcribed_result(preprocessed_text)

        self.db.insert(
            user_id = user_id, 
            transcribed_text = result['text'], 
            translated_text = result['translated_text'], 
            calories = result['calories'], 
            food_table = result['table'], 
            timestamp = datetime.datetime.utcnow().timestamp(),
            date = str(datetime.date.today()),
            time = str(datetime.datetime.now().time()))
        

    def process_transcribed_result(self, result):
        result = ast.literal_eval(result.replace('\n', ''))
        # convert 1,360 kcal to 1360
        result['calories'] = int(re.sub(r"\D", "", result['total_calorie']))
        return result

    def __del__(self):
        self.db.close()