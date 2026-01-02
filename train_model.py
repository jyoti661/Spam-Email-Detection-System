import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import joblib

print("Starting model training...")  # Debug print

# Load dataset
df = pd.read_csv("spam.csv", encoding="latin-1")[["v1", "v2"]]
df = df.rename(columns={"v1": "label", "v2": "text"})
df["label"] = df["label"].map({"ham": 0, "spam": 1})

# Split data into train and test
X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42
)

# Create ML pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english")),
    ("nb", MultinomialNB())
])

# Train the model
model.fit(X_train, y_train)

# Save the trained model to a file
joblib.dump(model, "spam_model.pkl")

print("✅ Model trained and saved as spam_model.pkl")  # Confirmation print
