import schedule
import time
import pytz
import os
from datetime import datetime
from news_fetcher import fetch_news
from stock_fetcher import fetch_top_stocks
from telegram_notifier import format_message, send_telegram_message

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TIMEZONE = pytz.timezone("Asia/Kuala_Lumpur")

def job():
    print(f"[{datetime.now()}] Starting scheduled job...")
    
    # Fetch Data
    world_news = fetch_news("world", 5)
    malaysia_news = fetch_news("malaysia", 5)
    world_stocks = fetch_top_stocks("world", 5)
    malaysia_stocks = fetch_top_stocks("malaysia", 5)
    
    # Format Message
    message = format_message(world_news, malaysia_news, world_stocks, malaysia_stocks)
    
    # Send
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        success = send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)
        if success:
            print(f"[{datetime.now()}] Report sent successfully.")
        else:
            print(f"[{datetime.now()}] Failed to send report.")
    else:
        print(f"[{datetime.now()}] Telegram credentials missing. Printing report to console:")
        print(message)

def run_scheduler():
    print(f"Scheduler started. Timezone: {TIMEZONE}")
    print("Waiting for 08:30 AM Asia/Kuala_Lumpur...")
    
    # Schedule the job
    # Note: schedule library uses system time. If system time is UTC, we need to adjust.
    # A robust way is to run every minute and check if it's 8:30 AM in KL.
    
    while True:
        # Get current time in KL
        kl_time = datetime.now(TIMEZONE)
        current_time_str = kl_time.strftime("%H:%M")
        
        # Check if it matches the target time (and we haven't run this minute yet)
        if current_time_str == "08:30":
            job()
            # Sleep for 61 seconds so we don't run it multiple times in the same minute
            time.sleep(61)
        
        # Sleep for 30 seconds before next check
        time.sleep(30)

if __name__ == "__main__":
    # For testing purposes, run immediately once, then start loop
    print("Running initial test job...")
    job()
    
    # Start the loop
    run_scheduler()
