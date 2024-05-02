import telebot
import vertexai
from vertexai.generative_models import GenerativeModel

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

# Start the bot
bot.polling(non_stop=True)
