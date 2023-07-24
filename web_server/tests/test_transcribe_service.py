import unittest
from unittest.mock import MagicMock, patch
from transcribe_service import TranscribeService
import os
os.environ['OPENAI_API_KEY'] = 'test_api_key'

class TranscribeServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.transcribe_service = TranscribeService()

    def test_summarize_calorie_intake(self):
        text = "I ate 100 calories bread"
        expected_result = {'total_calorie': 400}

        # Mock the SequentialChain and its output
        with patch('transcribe_service.SequentialChain') as mock_sequential_chain:
            mock_chain_instance = mock_sequential_chain.return_value
            mock_chain_instance.return_value = {"text": '早上吃了一碗肉松稀饭，中午吃了一个大的意大利sandwich，晚上吃了一碗米饭，两个小的猪排，半盘蔬菜，十片清真鳕鱼，小半个甜瓜', "table": "\n\n[{\"name\": '肉松稀饭', \"amount\": '1碗', \"calorie\": 400}]"}

            # Call the method under test
            result = self.transcribe_service.summarize_calorie_intake(text)

            # Assert the result
            self.assertEqual(result, expected_result)

    def test_transcribe_audio_file(self):
        file_name = "sample_audio.webm"
        expected_result = "今天早上吃了三个小笼包"

        # Mock the openai.Audio.transcribe() method and open the audio file
        with patch('builtins.open') as mock_open, \
             patch('transcribe_service.openai.Audio.transcribe') as mock_transcribe:
            mock_transcribe.return_value = MagicMock(text=expected_result)
            mock_file = MagicMock()
            mock_open.return_value.__enter__.return_value = mock_file

            # Call the method under test
            result = self.transcribe_service.transcribe_audio_file(file_name)

            # Assert the result
            self.assertEqual(result, expected_result)

    def test_process_transcribed_result(self):
        result = """\n\n[{'name': '肉松稀饭', 'amount': '1碗', 'calorie': 400}, {'name': '意大利sandwich', 'amount': '1个', 'calorie': 500}, {'name': '米饭', 'amount': '1碗', 'calorie': 250}, {'name': '猪排', 'amount': '2个', 'calorie': 400}, {'name': '蔬菜', 'amount': '半盘', 'calorie': 100}, {'name': '清真鳕鱼', 'amount': '10片', 'calorie': 200}, {'name': '甜瓜', 'amount': '小半个', 'calorie': 50}]"""

        expected_result = {
            'total_calorie': 1900
        }

        processed_result = self.transcribe_service.process_transcribed_result(result)

        self.assertEqual(processed_result, expected_result)

if __name__ == '__main__':
    unittest.main()
