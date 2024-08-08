import requests
import json
import os

# Replace with your bot's token
TELEGRAM_BOT_TOKEN = '7460298642:AAHQm98WrgfKMg8YuvlaB2v4TijkE_P8qHU'

# File to store chat IDs
CHAT_IDS_FILE = 'chat_ids.json'

def load_chat_ids():
    if os.path.exists(CHAT_IDS_FILE):
        with open(CHAT_IDS_FILE, 'r') as file:
            try:
                return set(json.load(file))
            except json.JSONDecodeError:
                return set()
    return set()

def send_message(message, chat_id):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=payload)
    try:
        response.raise_for_status()  # Check if the request was successful
        print(f"Message sent successfully to {chat_id}")
    except requests.exceptions.HTTPError as err:
        print(f"Error sending message to {chat_id}: {err}")
        print(response.json())  # Print the error message from Telegram

def send_message_to_all(message):
    chat_ids = load_chat_ids()
    for chat_id in chat_ids:
        send_message(message, chat_id)

def interactive_cli():
    print("Interactive CLI for Telegram Bot. Type 'exit' to quit.")
    while True:
        message = input("Enter your message: ")
        if message.lower() == 'exit':
            print("Exiting CLI.")
            break
        send_message_to_all(message)

if __name__ == "__main__":
    interactive_cli()
