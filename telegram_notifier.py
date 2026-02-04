import requests
import os

TELEGRAM_API_URL = "https://api.telegram.org/bot{}/sendMessage"

def format_message(world_news, malaysia_news, world_stocks, malaysia_stocks):
    """
    Formats the data into a readable message for Telegram.
    """
    message = "🌍 *DAILY INSIGHT REPORT* 🇲🇾\n\n"
    
    # World News
    message += "📰 *TOP 5 WORLD NEWS*\n"
    for i, news in enumerate(world_news, 1):
        # Escape markdown characters if necessary, keep it simple for now
        title = news['title'].replace('*', '').replace('_', '')
        source = news['source']
        link = news['link']
        message += f"{i}. [{title}]({link}) - _{source}_\n"
    message += "\n"
    
    # Malaysia News
    message += "📰 *TOP 5 MALAYSIA NEWS*\n"
    for i, news in enumerate(malaysia_news, 1):
        title = news['title'].replace('*', '').replace('_', '')
        source = news['source']
        link = news['link']
        message += f"{i}. [{title}]({link}) - _{source}_\n"
    message += "\n"
    
    # World Stocks
    message += "📈 *TOP 5 WORLD STOCKS (Movers)*\n"
    for i, stock in enumerate(world_stocks, 1):
        symbol = stock['ticker']
        price = stock['price']
        change_pct = stock['pct_change']
        emoji = "🟢" if change_pct >= 0 else "🔴"
        message += f"{i}. {symbol}: {price:.2f} ({emoji} {change_pct:+.2f}%)\n"
    message += "\n"

    # Malaysia Stocks
    message += "📈 *TOP 5 MALAYSIA STOCKS (Movers)*\n"
    for i, stock in enumerate(malaysia_stocks, 1):
        symbol = stock['ticker']
        price = stock['price']
        change_pct = stock['pct_change']
        emoji = "🟢" if change_pct >= 0 else "🔴"
        message += f"{i}. {symbol}: {price:.2f} ({emoji} {change_pct:+.2f}%)\n"
    
    return message

def send_telegram_message(bot_token, chat_id, message):
    """
    Sends the formatted message to the specified Telegram chat.
    """
    if not bot_token or not chat_id:
        print("Telegram Bot Token or Chat ID not provided. Skipping send.")
        return False

    url = TELEGRAM_API_URL.format(bot_token)
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Message sent successfully!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")
        return False

if __name__ == "__main__":
    # Test with dummy data
    dummy_news = [{"title": "Test News", "link": "http://example.com", "source": "BBC"}] * 5
    dummy_stocks = [{"ticker": "AAPL", "price": 150.00, "pct_change": 1.5}] * 5
    
    msg = format_message(dummy_news, dummy_news, dummy_stocks, dummy_stocks)
    print("--- GENERATED MESSAGE PREVIEW ---")
    print(msg)
    
    # Uncomment to test real sending (requires env vars)
    # token = os.getenv("TELEGRAM_BOT_TOKEN")
    # chat_id = os.getenv("TELEGRAM_CHAT_ID")
    # send_telegram_message(token, chat_id, msg)
