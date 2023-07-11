from sqlite_db import SQLiteDB
import ast
import datetime

class TranscribeService:
    def __init__(self):
        self.db = SQLiteDB('mydatabase.db')

    def transcribe_and_insert(self, user_id):
        # Perform transcription using OpenAI Whisper API
        result = self.process_transcribed_result(self.transcribe_audio())

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
        result['calories'] = int(result['total_calorie'].lower().strip().replace('kcal','').replace(",", ""))
        return result

    def transcribe_audio(self):
        # Transcribe the audio using OpenAI Whisper API
        # Replace this with your actual transcription logic
        return '''{'text': '今天早上我吃了一碗粥,一个粽子 中午吃了一碗米饭,一些红烧肉和一些蔬菜 晚上吃了一碗米饭,几块烤鸭 一些红烧肉和一些蔬菜 还吃了两个小橘子,两个小的无花果', 'translated_text': '\n\nThis morning I had a bowl of porridge and a zongzi. For lunch I had a bowl of rice, some braised pork and some vegetables. For dinner I had a bowl of rice, a few pieces of roast duck, some braised pork and some vegetables. I also had two small oranges and two small figs.', 'table': '\n\n|Food Name|Amount|Estimate Calorie|\n|---|---|---|\n|Porridge|1 bowl|200 kcal|\n|Zongzi|1|200 kcal|\n|Rice|2 bowls|400 kcal|\n|Braised Pork|2 servings|400 kcal|\n|Vegetables|2 servings|100 kcal|\n|Roast Duck|2 pieces|200 kcal|\n|Oranges|2 small|80 kcal|\n|Figs|2 small|80 kcal|', 'total_calorie': '\n\n1,360 kcal'}'''


# Example usage:
if __name__ == '__main__':
    transcribe_service = TranscribeService()

    transcribed_text = transcribe_service.transcribe_and_insert(100)
    print(transcribe_service.db.get_items())
    transcribe_service.db.close()
