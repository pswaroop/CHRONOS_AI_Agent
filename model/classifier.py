from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Add manual or semi-automated labeling to scraped data
# For demo, assign a default label (could later use rule-based tagging)
df['label'] = "neutral"  # Placeholder label

X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.25)

model = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', max_df=0.7)),
    ('clf', MultinomialNB())
])

model.fit(X_train, y_train)
print("Model trained on scraped news. Accuracy:", model.score(X_test, y_test))