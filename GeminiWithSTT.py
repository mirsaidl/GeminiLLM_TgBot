import telebot
import vertexai
from vertexai.generative_models import GenerativeModel
# Voice recognition
import os
from google.cloud import speech_v1p1beta1 as speech

# Initialize the Telegram bot with your token
bot = telebot.TeleBot("TELEGRAM_BOT_TOKEN")

# Initialize Vertex AI
vertexai.init(project="VERTEX-AI PROJECT ID", location="LOCATION")

# Load the model
multimodal_model = GenerativeModel(model_name="gemini-1.0-pro-vision-001") # you can use other models of google cloud

# Maximum length of a Telegram message
MAX_MESSAGE_LENGTH = 4096

# Handle messages
@bot.message_handler(content_types=['text'])
def handle_message(message):
    try:
        # Check if the message contains text
        if message.text:
            query = message.text
            bot.send_chat_action(message.chat.id, 'typing')
            response = multimodal_model.generate_content([query])
            response_text = response.text[:MAX_MESSAGE_LENGTH]  # Truncate response if it's too long
            bot.reply_to(message, response_text)        
    except ValueError as e:
        print(f"Error: {e}")
        bot.reply_to(message, "Sorry, I couldn't generate a response. Please try again.")

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    try:
        if message.voice:
            # Create a client for the Speech-to-Text API
            client = speech.SpeechClient()

            # Specify the path to the voice file
            voice_file_path = "voice.ogg"

            # Read the voice file
            with open(voice_file_path, "rb") as audio_file:
                content = audio_file.read()

            # Configure the audio settings
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
                sample_rate_hertz=16000,
                language_code="en-US",
            )

            # Transcribe the voice to text
            response = client.recognize(config=config, audio=audio)

            # Get the transcribed text
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript

            # Use the transcribed text in your code
            response = multimodal_model.generate_content([transcript])
            response_text = response.text[:MAX_MESSAGE_LENGTH]  # Truncate response if it's too long
            bot.reply_to(message, response_text)

            # Remove the voice file
            os.remove(voice_file_path)
    except ValueError as e:
        print(f"Error: {e}")
        bot.reply_to(message, "Sorry, I couldn't generate a response. Please try again.")

# Start the bot
bot.polling(non_stop=True)
