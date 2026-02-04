import streamlit as st
import pandas as pd
from news_fetcher import fetch_news
from stock_fetcher import fetch_top_stocks

st.set_page_config(page_title="Daily Insight Dashboard", layout="wide")

st.title("🌍 Daily Insight Dashboard 🇲🇾")
st.markdown("Automated insights for World & Malaysia News and Stocks")

if st.button("Refresh Data"):
    st.rerun()

col1, col2 = st.columns(2)

with col1:
    st.header("📰 World News")
    with st.spinner("Fetching World News..."):
        world_news = fetch_news("world", 5)
        for news in world_news:
            st.subheader(f"[{news['title']}]({news['link']})")
            st.caption(f"Source: {news['source']} | Score: {news['score']}")
            st.write(news['summary'])
            st.divider()

    st.header("📈 World Stocks (Movers)")
    with st.spinner("Fetching World Stocks..."):
        world_stocks = fetch_top_stocks("world", 5)
        if world_stocks:
            df_world = pd.DataFrame(world_stocks)
            # Format percentage
            df_world['Change'] = df_world['pct_change'].apply(lambda x: f"{x:+.2f}%")
            df_world['Price'] = df_world['price'].apply(lambda x: f"{x:.2f}")
            st.dataframe(
                df_world[['ticker', 'Price', 'Change']], 
                hide_index=True, 
                use_container_width=True
            )
        else:
            st.error("Failed to fetch stock data")

with col2:
    st.header("📰 Malaysia News")
    with st.spinner("Fetching Malaysia News..."):
        my_news = fetch_news("malaysia", 5)
        for news in my_news:
            st.subheader(f"[{news['title']}]({news['link']})")
            st.caption(f"Source: {news['source']} | Score: {news['score']}")
            st.write(news['summary'])
            st.divider()

    st.header("📈 Malaysia Stocks (Movers)")
    with st.spinner("Fetching Malaysia Stocks..."):
        my_stocks = fetch_top_stocks("malaysia", 5)
        if my_stocks:
            df_my = pd.DataFrame(my_stocks)
            df_my['Change'] = df_my['pct_change'].apply(lambda x: f"{x:+.2f}%")
            df_my['Price'] = df_my['price'].apply(lambda x: f"{x:.2f}")
            st.dataframe(
                df_my[['ticker', 'Price', 'Change']], 
                hide_index=True, 
                use_container_width=True
            )
        else:
            st.error("Failed to fetch stock data")

st.markdown("---")
st.caption("Data sources: Yahoo Finance, RSS Feeds (BBC, CNN, The Star, Malay Mail)")
