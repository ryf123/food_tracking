import os
import openai
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
class TranscribeService:
	def __init__(self):
		openai.api_key = os.getenv("OPENAI_API_KEY")

	def summarize_calorie_intake(self, text):
		llm = OpenAI(temperature=0)
		translate_template = """Translate the text to English: {text} """
		translate_prompt_template = PromptTemplate(input_variables=["text"], template=translate_template)
		translate_chain = LLMChain(llm=llm, prompt=translate_prompt_template, output_key="translated_text")

		estimate_calorie_template = """Estimate the calorie for each item, and put them in a table with format, |food_name|amount|estimate calorie|: {translated_text} """
		estimate_calorie_prompt_template = PromptTemplate(input_variables=["translated_text"], template=estimate_calorie_template)
		estimate_calorie_chain = LLMChain(llm=llm, prompt=estimate_calorie_prompt_template, output_key="table")

		total_calorie_chain_tempate = """Sum the estimated total calorie taken in the table: {table}"""
		total_calorie_prompt_template = PromptTemplate(input_variables=["table"], template=total_calorie_chain_tempate)
		total_calorie_chain = LLMChain(llm=llm, prompt=total_calorie_prompt_template, output_key="total_calorie")

		overall_chain = SequentialChain(chains=[translate_chain, estimate_calorie_chain, total_calorie_chain], input_variables=["text"], output_variables=["translated_text", "table", "total_calorie"], verbose=True)
		result = overall_chain({'text': text})
		print(result)
		return result

	def transcribe_audio(self):
		# Transcribe the audio using OpenAI Whisper API
		# Replace this with your actual transcription logic
		try:
			audio_file= open("/Users/yifei/Downloads/recorded_audio.webm", "rb")
			transcript = openai.Audio.transcribe("whisper-1", audio_file, prompt="The input is related to food consumed on a specific day")
			return transcript.text
		except Exception as e:
			print("An error occurred:", str(e))
			return '''{'text': '今天早上我吃了一碗粥,一个粽子 中午吃了一碗米饭,一些红烧肉和一些蔬菜 晚上吃了一碗米饭,几块烤鸭 一些红烧肉和一些蔬菜 还吃了两个小橘子,两个小的无花果', 'translated_text': '\n\nThis morning I had a bowl of porridge and a zongzi. For lunch I had a bowl of rice, some braised pork and some vegetables. For dinner I had a bowl of rice, a few pieces of roast duck, some braised pork and some vegetables. I also had two small oranges and two small figs.', 'table': '\n\n|Food Name|Amount|Estimate Calorie|\n|---|---|---|\n|Porridge|1 bowl|200 kcal|\n|Zongzi|1|200 kcal|\n|Rice|2 bowls|400 kcal|\n|Braised Pork|2 servings|400 kcal|\n|Vegetables|2 servings|100 kcal|\n|Roast Duck|2 pieces|200 kcal|\n|Oranges|2 small|80 kcal|\n|Figs|2 small|80 kcal|', 'total_calorie': '\n\n1,360 kcal'}'''