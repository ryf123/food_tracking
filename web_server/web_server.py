import http.server
import socketserver
import os
import openai
import json
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain

# Define the port number for the server to listen on
PORT = 8000

# Create a request handler by inheriting from the SimpleHTTPRequestHandler class
class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    # Override the log_message() method to suppress log messages
    def log_message(self, format, *args):
        return

    # Override the do_GET() method to customize the homepage
    def do_GET(self):
        if self.path == "/":
            # Customize the content for the homepage
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open('homepage.html', 'r') as f:
                self.wfile.write(bytes(f.read(), encoding='utf-8'))
        elif self.path == "/transcribe":
            self.send_response(200)
            openai.api_key = os.getenv("OPENAI_API_KEY")

            text = self.transcribe()
            print(text)
            calories = self.summarize_calorie_intake(text)
            print(calories)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps({'calories': calories}), 'utf-8'))
        else:
            super().do_GET()

    def transcribe(self):
        try:
            audio_file= open("/Users/yifei/Downloads/recorded_audio.webm", "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file, prompt="The input is related to food consumed on a specific day")
            return transcript.text
        except Exception as e:
            print("An error occurred:", str(e))

    def summarize_calorie_intake(self, text):
        llm = OpenAI(temperature=0)
        translate_template = """Translate the text to English: {text} """
        translate_prompt_template = PromptTemplate(input_variables=["text"], template=translate_template)
        translate_chain = LLMChain(llm=llm, prompt=translate_prompt_template)

        estimate_calorie_template = """Estimate the calorie for each item, and put them in a table with format, |food_name|amount|estimate calorie|: {translated_text} """
        estimate_calorie_prompt_template = PromptTemplate(input_variables=["translated_text"], template=estimate_calorie_template)
        estimate_calorie_chain = LLMChain(llm=llm, prompt=estimate_calorie_prompt_template)

        total_calorie_chain_tempate = """Sum the estimated total calorie taken in the table: {table}"""
        total_calorie_prompt_template = PromptTemplate(input_variables=["table"], template=total_calorie_chain_tempate)
        total_calorie_chain = LLMChain(llm=llm, prompt=total_calorie_prompt_template)

        overall_chain = SimpleSequentialChain(chains=[translate_chain, estimate_calorie_chain, total_calorie_chain], verbose=True)
        return overall_chain.run(text).strip('\n')

    def completion(self, prompt):
      try:
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt=prompt,
          max_tokens=200
        )
        print(response)
        completion = response.choices[0].text.strip()
        return completion
      except Exception as e:
        print("An error occurred:", str(e))

# Create an instance of the HTTP server with the defined port and request handler
with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
    print(f"Server running on port {PORT}")
    # Start the server and keep it running until interrupted
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer interrupted. Stopping...")
        httpd.server_close()