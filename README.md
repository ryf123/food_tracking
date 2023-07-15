# Calorie Tracker Web Application

This is a web application developed to track calorie consumption using ChatGPT.

## Introduction

The goal of this application is to provide users with an interface to interact and track their calorie intake. Users can input their calorie information either by voice or text. The application utilizes the Whisper API from OpenAI to transcribe the text and the Chat API to calculate the calorie content. The data is then stored in a local database.

## Components

The application consists of the following components:

- User interface: The user interface is built using HTML and JavaScript.
- Transcribe service: Utilizes the Whisper API for text transcription.
- API interface: Handles communication between the client and server.
- Database interface: Handles database operations using SQLLite.

## Usage

To use the application, follow these steps:

1. Start the Python simple HTTP server to serve the web traffic, you will need to export your API key to env, export OPENAI_API_KEY="your_key"
2. Access the web application through the URL http://localhost:8000/.
3. Use the user interface to record calorie information using voice or text.
4. The application will transcribe the text, calculate the calorie content, and save the data to the local database.
5. The data can be accessed and viewed through the dashboard, http://localhost:8000/dashboard.

## Installation

1. Clone the repository to your local machine.
2. Install the required dependencies listed in the `requirements.txt` file.
3. Start the Python server to serve the web traffic.
4. Access the web application through the provided URL.

## Contributing

Contributions to this project are welcome. If you encounter any issues or have suggestions for improvements, please feel free to submit a pull request or open an issue.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or further information, please contact [your-name] at [your-email-address].

