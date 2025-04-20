from model import classifier

def predict_opinion(news_text):
    return classifier.predict([news_text])[0]

def generate_response_with_model(question, related_news_text):
    tone = predict_opinion(related_news_text)
    return f"ChronoSage [{tone.upper()} take]: {related_news_text[:150]}..."

# Example Usage (if articles are found)
if not df.empty:
    sample_news = df.iloc[0]['text']
    response = generate_response_with_model("What’s happening in Ukraine?", sample_news)
    print("\nChronoSage Response:\n", response)
else:
    print("No news articles found for today.")