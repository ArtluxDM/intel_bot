import requests
import feedparser
import json
import os

# Replace with your bot's token
TELEGRAM_BOT_TOKEN ={your telegram bot API key}

# File to store chat IDs
CHAT_IDS_FILE = 'chat_ids.json'

# URLs of RSS feeds
RSS_FEEDS = [
     'https://grahamcluley.com/feed',
     'https://feeds.feedburner.com/TheHackersNews',
     'https://www.csoonline.com/feed/',
     'https://www.schneier.com/feed/atom/'
]

# File to store sent titles and latest news
SENT_TITLES_FILE = 'sent_titles.json'
LATEST_NEWS_FILE = 'latest_news.json'

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

def load_sent_titles():
    if os.path.exists(SENT_TITLES_FILE):
        with open(SENT_TITLES_FILE, 'r') as file:
            try:
                return set(json.load(file))
            except json.JSONDecodeError:
                return set()
    return set()

def save_sent_titles(sent_titles):
    with open(SENT_TITLES_FILE, 'w') as file:
        json.dump(list(sent_titles), file)

def load_latest_news():
    if os.path.exists(LATEST_NEWS_FILE):
        with open(LATEST_NEWS_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_latest_news(news_items):
    with open(LATEST_NEWS_FILE, 'w') as file:
        json.dump(news_items, file)

def fetch_news():
    news_items = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:  # Get top 3 news items from each feed
            news_items.append({
                'title': entry.title,
                'link': entry.link
            })
    return news_items

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

def get_new_chat_ids():
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates'
    response = requests.get(url)
    data = response.json()

    new_chat_ids = set()
    for result in data['result']:
        if 'message' in result and 'chat' in result['message']:
            new_chat_ids.add(result['message']['chat']['id'])

    return new_chat_ids

def main(test_mode=False):
    # Load previously sent titles and chat IDs
    sent_titles = load_sent_titles()
    chat_ids = load_chat_ids()
    
    # Fetch new chat IDs from the bot updates
    new_chat_ids = get_new_chat_ids()
    
    # Update chat IDs with any new chat IDs
    chat_ids.update(new_chat_ids)
    save_chat_ids(chat_ids)
    
    # Fetch the latest news
    news_items = fetch_news()
    
    # Filter out news items that were already sent
    new_news_items = [item for item in news_items if item['title'] not in sent_titles]
    
    if new_news_items:
        # Prepare message with new news items
        message = "*Top Cybersecurity News for Today:*\n\n" + "\n\n".join([f"[{item['title']}]({item['link']})" for item in new_news_items])
        
        # Update sent titles and latest news
        sent_titles.update(item['title'] for item in new_news_items)
        save_sent_titles(sent_titles)
        save_latest_news(new_news_items)
    else:
        # Load the latest news if there are no new news items
        latest_news_items = load_latest_news()
        if latest_news_items:
            message = "*No new cybersecurity news items today. Here are the latest news items:*\n\n" + "\n\n".join([f"[{item['title']}]({item['link']})" for item in latest_news_items])
        else:
            message = "There are no new cybersecurity news items today."

    if test_mode:
        # Print the message to the console instead of sending it
        print(message)
    else:
        # Send the message to all chat IDs
        for chat_id in chat_ids:
            send_message(message, chat_id)

if __name__ == "__main__":
    # Run the script in test mode
    main(test_mode=False)
