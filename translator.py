from deep_translator import GoogleTranslator

def translate_text(text, target="zh-CN"):
    """
    Translates text to the target language using Google Translate (free).
    """
    if not text:
        return ""
    try:
        # Use simple caching or just direct call. 
        # deep_translator is robust enough for small batches.
        translated = GoogleTranslator(source='auto', target=target).translate(text)
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def translate_news_item(news_item, target="zh-CN"):
    """
    Translates the title and summary of a news item.
    """
    news_item_copy = news_item.copy()
    news_item_copy['title_translated'] = translate_text(news_item['title'], target)
    # Summaries can be long, maybe just translate title to save time/limits?
    # Let's try translating summary too but keep it short.
    if news_item['summary']:
        news_item_copy['summary_translated'] = translate_text(news_item['summary'][:500], target)
    else:
        news_item_copy['summary_translated'] = ""
    return news_item_copy

if __name__ == "__main__":
    # Test
    print(translate_text("Hello, world!", "zh-CN"))