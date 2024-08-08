import requests
import json
import os

# Replace with your bot's token
TELEGRAM_BOT_TOKEN = {your bot API key}

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

def save_chat_ids(chat_ids):
    with open(CHAT_IDS_FILE, 'w') as file:
        json.dump(list(chat_ids), file)

def get_new_chat_ids():
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates'
    response = requests.get(url)
    data = response.json()

    new_chat_ids = set()
    for result in data['result']:
        if 'message' in result and 'chat' in result['message']:
            new_chat_ids.add(result['message']['chat']['id'])

    return new_chat_ids

def update_chat_ids():
    # Load previously stored chat IDs
    chat_ids = load_chat_ids()
    
    # Fetch new chat IDs from the bot updates
    new_chat_ids = get_new_chat_ids()
    
    # Update chat IDs with any new chat IDs
    chat_ids.update(new_chat_ids)
    save_chat_ids(chat_ids)
    
    # Print the updated chat IDs to verify
    print(f"Updated Chat IDs: {chat_ids}")

if __name__ == "__main__":
    update_chat_ids()
