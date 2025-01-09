from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pandas as pd

# Load the clothing data
clothing_data = pd.read_csv('data/clothing_data.csv')

# Sample model: Train on existing reviews to predict recommendations
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(clothing_data['review_text'].fillna(''))
y = clothing_data['Recommended'].fillna(0)  # Assuming binary (0 or 1) labels

model = LogisticRegression()
model.fit(X, y)

def recommend_item(review_text):
    """Predict if an item is recommended based on the review."""
    X_new = vectorizer.transform([review_text])
    prediction = model.predict(X_new)[0]
    return str(prediction)
