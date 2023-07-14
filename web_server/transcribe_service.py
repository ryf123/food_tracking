import os
import openai
import re
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
class TranscribeService:
	def __init__(self):
		openai.api_key = os.getenv("OPENAI_API_KEY")

	def summarize_calorie_intake(self, text):
		llm = OpenAI(temperature=0)

		estimate_calorie_template = """Estimate the calorie for each item, and put them in a table with format, |food_name|amount|estimate calorie|: {text} """
		estimate_calorie_prompt_template = PromptTemplate(input_variables=["text"], template=estimate_calorie_template)
		estimate_calorie_chain = LLMChain(llm=llm, prompt=estimate_calorie_prompt_template, output_key="table")

		total_calorie_chain_tempate = """Given table: {table}, sum the number in 'estimate calorie' column and return the result only in digits, do not multiply column amount and estimate calorie"""
		total_calorie_prompt_template = PromptTemplate(input_variables=["table"], template=total_calorie_chain_tempate)
		total_calorie_chain = LLMChain(llm=llm, prompt=total_calorie_prompt_template, output_key="total_calorie")

		overall_chain = SequentialChain(chains=[estimate_calorie_chain, total_calorie_chain], input_variables=["text"], output_variables=["table", "total_calorie"], verbose=True)
		result = overall_chain({'text': text})
		processed_result = self.process_transcribed_result(result)
		print(processed_result)
		return processed_result

	def process_transcribed_result(self, result):
		# convert 1,360 kcal to 1360
		result['total_calorie'] = int(re.sub(r"\D", "", result['total_calorie']))
		return result

	def transcribe_audio(self, audio_content):
		# Transcribe the audio using OpenAI Whisper API
		# Replace this with your actual transcription logic
		try:
			transcript = openai.Audio.transcribe("whisper-1", audio_content, prompt="The input is related to food consumed on a specific day")
			return transcript.text
		except Exception as e:
			print("An error occurred:", str(e))

	def transcribe_audio_file(self, file_name):
		# Transcribe the audio using OpenAI Whisper API
		# Replace this with your actual transcription logic
		try:
			audio_file= open(file_name, "rb")
			transcript = openai.Audio.transcribe("whisper-1", audio_file, prompt="The input is related to food consumed on a specific day")
			return transcript.text
		except Exception as e:
			print("An error occurred:", str(e))
