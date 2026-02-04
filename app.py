import streamlit as st
import pandas as pd
from news_fetcher import fetch_news
from stock_fetcher import fetch_top_stocks
from translator import translate_text

st.set_page_config(page_title="Daily Insight Dashboard", layout="wide")

# Language Selection
lang = st.sidebar.radio("Language / 语言", ["English", "中文 (Chinese)"])
is_chinese = lang == "中文 (Chinese)"

# UI Labels
LABELS = {
    "title": "🌍 Daily Insight Dashboard 🇲🇾" if not is_chinese else "🌍 每日财经洞察 🇲🇾",
    "subtitle": "Automated insights for World & Malaysia News and Stocks" if not is_chinese else "全球与马来西亚新闻及股票自动分析",
    "refresh": "Refresh Data" if not is_chinese else "刷新数据",
    "world_news": "📰 World News" if not is_chinese else "📰 国际新闻",
    "world_stocks": "📈 World Stocks (Movers)" if not is_chinese else "📈 国际股票 (异动)",
    "my_news": "📰 Malaysia News" if not is_chinese else "📰 马来西亚新闻",
    "my_stocks": "📈 Malaysia Stocks (Movers)" if not is_chinese else "📈 马来西亚股票 (异动)",
    "source": "Source" if not is_chinese else "来源",
    "score": "Score" if not is_chinese else "评分",
    "price": "Price" if not is_chinese else "价格",
    "change": "Change" if not is_chinese else "涨跌幅",
    "loading": "Fetching Data..." if not is_chinese else "正在获取数据...",
    "error": "Failed to fetch data" if not is_chinese else "获取数据失败"
}

st.title(LABELS["title"])
st.markdown(LABELS["subtitle"])

if st.button(LABELS["refresh"]):
    st.rerun()

col1, col2 = st.columns(2)

def display_news(news_list):
    for news in news_list:
        title = news['title']
        summary = news['summary']
        
        if is_chinese:
            # On-the-fly translation (caching recommended for prod, but Streamlit reruns might make it slow without st.cache_data)
            # We use a simple caching decorator if this were a heavy app, but for 5 items it's okay-ish.
            # To improve UX, we can show original first, then replace.
            title = translate_text(title, "zh-CN")
            summary = translate_text(summary[:300], "zh-CN") # Limit summary length

        st.subheader(f"[{title}]({news['link']})")
        st.caption(f"{LABELS['source']}: {news['source']} | {LABELS['score']}: {news['score']}")
        st.write(summary)
        st.divider()

with col1:
    st.header(LABELS["world_news"])
    with st.spinner(LABELS["loading"]):
        world_news = fetch_news("world", 5)
        display_news(world_news)

    st.header(LABELS["world_stocks"])
    with st.spinner(LABELS["loading"]):
        world_stocks = fetch_top_stocks("world", 5)
        if world_stocks:
            df_world = pd.DataFrame(world_stocks)
            df_world[LABELS['change']] = df_world['pct_change'].apply(lambda x: f"{x:+.2f}%")
            df_world[LABELS['price']] = df_world['price'].apply(lambda x: f"{x:.2f}")
            st.dataframe(
                df_world[['ticker', LABELS['price'], LABELS['change']]], 
                hide_index=True, 
                use_container_width=True
            )
        else:
            st.error(LABELS["error"])

with col2:
    st.header(LABELS["my_news"])
    with st.spinner(LABELS["loading"]):
        my_news = fetch_news("malaysia", 5)
        display_news(my_news)

    st.header(LABELS["my_stocks"])
    with st.spinner(LABELS["loading"]):
        my_stocks = fetch_top_stocks("malaysia", 5)
        if my_stocks:
            df_my = pd.DataFrame(my_stocks)
            df_my[LABELS['change']] = df_my['pct_change'].apply(lambda x: f"{x:+.2f}%")
            df_my[LABELS['price']] = df_my['price'].apply(lambda x: f"{x:.2f}")
            st.dataframe(
                df_my[['ticker', LABELS['price'], LABELS['change']]], 
                hide_index=True, 
                use_container_width=True
            )
        else:
            st.error(LABELS["error"])

st.markdown("---")
st.caption("Data sources: Yahoo Finance, RSS Feeds | Translation: Google Translate")