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
        expected_result = {'total_calorie': 100}

        # Mock the SequentialChain and its output
        with patch('transcribe_service.SequentialChain') as mock_sequential_chain:
            mock_chain_instance = mock_sequential_chain.return_value
            mock_chain_instance.return_value = {"total_calorie": '100'}

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
        result = {
            'text': 'I ate an apple',
            'total_calorie': '1,360 kcal'
        }

        expected_result = {
            'total_calorie': 1360,
            'text': 'I ate an apple'
        }

        processed_result = self.transcribe_service.process_transcribed_result(result)

        self.assertEqual(processed_result, expected_result)

if __name__ == '__main__':
    unittest.main()
