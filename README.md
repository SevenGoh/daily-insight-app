# Daily Insight App 🌍🇲🇾

This application automatically fetches the most important World & Malaysia News and Stocks every day at 8:30 AM (Malaysia Time) and sends a summary via Telegram. It also includes a web dashboard to view the insights on demand.

## Features
- **Smart News Selection:** Uses keyword scoring to pick "important" news (economy, policy, crisis, etc.) rather than just the latest headlines.
- **Stock Movers:** Identifies top volatile stocks/indices in World (US Markets) and Malaysia (Bursa).
- **Telegram Bot:** Auto-sends the report every morning.
- **Web Dashboard:** Simple UI to view the latest data.

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Telegram Bot
1.  Open Telegram and search for `@BotFather`.
2.  Send `/newbot` and follow instructions to get a **Bot Token**.
3.  Start a chat with your new bot and get your **Chat ID** (you can use `@userinfobot` to find your ID).
4.  Set environment variables:
    ```bash
    export TELEGRAM_BOT_TOKEN="your_bot_token_here"
    export TELEGRAM_CHAT_ID="your_chat_id_here"
    ```

### 3. Run the Scheduler (for Auto-Sending)
Run this script in the background on your server/computer. It will check the time and send the report at 8:30 AM Malaysia time.
```bash
python daily_insight_app/scheduler.py
```

### 4. Run the Dashboard (Optional)
To view the data in your browser:
```bash
streamlit run daily_insight_app/app.py
```

## Customization
- **Feeds:** Edit `daily_insight_app/news_fetcher.py` to add more RSS feeds.
- **Stocks:** Edit `daily_insight_app/stock_fetcher.py` to add more tickers.
- **Keywords:** Edit `daily_insight_app/news_fetcher.py` to change scoring logic.
