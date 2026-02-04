import os
import sys
from news_fetcher import fetch_news
from stock_fetcher import fetch_top_stocks
from telegram_notifier import format_bilingual_message, send_telegram_message

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def run_once():
    print("Starting Daily Insight Job (Bilingual Run)...")
    
    # Fetch Data
    world_news = fetch_news("world", 5)
    malaysia_news = fetch_news("malaysia", 5)
    world_stocks = fetch_top_stocks("world", 5)
    malaysia_stocks = fetch_top_stocks("malaysia", 5)
    
    # Format Message (Bilingual)
    message = format_bilingual_message(world_news, malaysia_news, world_stocks, malaysia_stocks)
    
    # Send
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        success = send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)
        if success:
            print("Report sent successfully.")
        else:
            print("Failed to send report.")
            sys.exit(1) # Fail the action if sending fails
    else:
        print("Telegram credentials missing. Printing report to console:")
        print(message)
        # We don't fail here because maybe the user just wants to see logs in Actions

if __name__ == "__main__":
    run_once()