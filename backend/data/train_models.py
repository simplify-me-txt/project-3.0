import pandas as pd
import pymongo
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import re
import os

# Config
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "ecommerce_db"
COLLECTION_NAME = "reviews"
MODEL_DIR = "backend/models"

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

def train_models():
    print("Connecting to MongoDB to fetch training data...")
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    # Fetch data (limit to 50k for training speed if needed, but project asked for 100k)
    # We'll use 20k for demo speed if it's too slow, but let's try full dataset first.
    # Actually, let's limit to 20k for the sake of response time in this interaction, 
    # but I'll write code to fetch all and maybe sample.
    cursor = collection.find({}, {"review_text": 1, "rating": 1, "_id": 0})
    df = pd.DataFrame(list(cursor))
    
    print(f"Loaded {len(df)} records.")
    
    # Create Sentiment Label
    # Rating 1,2 -> Negative (0), 3 -> Neutral (1), 4,5 -> Positive (2)
    
    def get_sentiment(rating):
        if rating <= 2: return 0
        if rating == 3: return 1
        return 2
        
    df['sentiment'] = df['rating'].apply(get_sentiment)
    
    print("Preprocessing text...")
    df['clean_text'] = df['review_text'].apply(clean_text)
    
    X = df['clean_text']
    y = df['sentiment']
    
    print(f"Class distribution: {y.value_counts()}")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Vectorizing data...")
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    models = {
        "logistic_regression": LogisticRegression(max_iter=1000, multi_class='multinomial'),
        "svm": LinearSVC(max_iter=1000), # LinearSVC supports multi-class by default via OvR
        "random_forest": RandomForestClassifier(n_estimators=50, max_depth=10, n_jobs=-1)
    }
    
    best_model = None
    best_acc = 0
    best_name = ""
    
    results = {}
    
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train_vec, y_train)
        preds = model.predict(X_test_vec)
        acc = accuracy_score(y_test, preds)
        print(f"{name} Accuracy: {acc:.4f}")
        results[name] = acc
        
        if acc > best_acc:
            best_acc = acc
            best_model = model
            best_name = name
            
    print(f"Best model: {best_name} with accuracy {best_acc:.4f}")
    
    # Save Best Model and Vectorizer
    joblib.dump(best_model, f"{MODEL_DIR}/sentiment_model.pkl")
    joblib.dump(vectorizer, f"{MODEL_DIR}/tfidf_vectorizer.pkl")
    
    # Save metadata
    with open(f"{MODEL_DIR}/model_metadata.txt", "w") as f:
        f.write(f"Best Model: {best_name}\n")
        f.write(f"Accuracy: {best_acc}\n")
        f.write(f"Trained on: {len(df)} samples\n")
        
    print("Model training complete and saved.")

if __name__ == "__main__":
    train_models()
