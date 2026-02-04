import requests
import os
from translator import translate_text

TELEGRAM_API_URL = "https://api.telegram.org/bot{}/sendMessage"

def format_bilingual_message(world_news, malaysia_news, world_stocks, malaysia_stocks):
    """
    Formats the data into a bilingual (English + Chinese) message for Telegram.
    """
    message = "🌍 *DAILY INSIGHT / 每日财经* 🇲🇾\n\n"
    
    # World News
    message += "📰 *WORLD NEWS / 国际新闻*\n"
    for i, news in enumerate(world_news, 1):
        title_en = news['title'].replace('*', '').replace('_', '')
        title_cn = translate_text(title_en, "zh-CN")
        link = news['link']
        
        message += f"{i}. [{title_en}]({link})\n"
        message += f"   🇨🇳 {title_cn}\n"
    message += "\n"
    
    # Malaysia News
    message += "📰 *MALAYSIA NEWS / 马来西亚新闻*\n"
    for i, news in enumerate(malaysia_news, 1):
        title_en = news['title'].replace('*', '').replace('_', '')
        title_cn = translate_text(title_en, "zh-CN")
        link = news['link']
        
        message += f"{i}. [{title_en}]({link})\n"
        message += f"   🇨🇳 {title_cn}\n"
    message += "\n"
    
    # World Stocks
    message += "📈 *WORLD STOCKS / 国际股票*\n"
    for i, stock in enumerate(world_stocks, 1):
        symbol = stock['ticker']
        price = stock['price']
        change_pct = stock['pct_change']
        emoji = "🟢" if change_pct >= 0 else "🔴"
        # Stocks don't really need translation, just universal format
        message += f"{i}. {symbol}: {price:.2f} ({emoji} {change_pct:+.2f}%)\n"
    message += "\n"

    # Malaysia Stocks
    message += "📈 *MALAYSIA STOCKS / 马来西亚股票*\n"
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
        "parse_mode": "Markdown",
        "disable_web_page_preview": True 
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
    dummy_news = [{"title": "Market hits record high", "link": "http://example.com", "source": "BBC"}] 
    dummy_stocks = [{"ticker": "AAPL", "price": 150.00, "pct_change": 1.5}]
    
    msg = format_bilingual_message(dummy_news, dummy_news, dummy_stocks, dummy_stocks)
    print("--- GENERATED MESSAGE PREVIEW ---")
    print(msg)