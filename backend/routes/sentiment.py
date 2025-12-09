from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import re
import os
from backend.database import get_database
import collections

router = APIRouter()

MODEL_PATH = "backend/models/sentiment_model.pkl"
VEC_PATH = "backend/models/tfidf_vectorizer.pkl"

model = None
vectorizer = None

class SentimentRequest(BaseModel):
    review_text: str
    model: str = "logistic_regression" # Ignored for now as we load best model

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float
    keywords: list

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

def load_model():
    global model, vectorizer
    if os.path.exists(MODEL_PATH) and os.path.exists(VEC_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            vectorizer = joblib.load(VEC_PATH)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Failed to load model: {e}")
    else:
        print("Model files not found. Prediction will fail.")

@router.post("/predict", response_model=SentimentResponse)
def predict_sentiment(request: SentimentRequest):
    if not model or not vectorizer:
        raise HTTPException(status_code=503, detail="Model not loaded")
        
    cleaned = clean_text(request.review_text)
    vec = vectorizer.transform([cleaned])
    
    # Predict
    pred = model.predict(vec)[0] # 0, 1, or 2
    prob = model.predict_proba(vec)[0] # [p0, p1, p2]
    
    sentiment_map = {0: "Negative", 1: "Neutral", 2: "Positive"}
    sentiment = sentiment_map.get(pred, "Neutral")
    confidence = prob[pred]
    
    # Simple keyword extraction (TF-IDF based would be better, but simple split for now)
    words = cleaned.split()
    # Filter stopwords logic omitted for brevity, just taking long words
    keywords = [w for w in words if len(w) > 4][:5]
    
    return SentimentResponse(
        sentiment=sentiment,
        confidence=float(confidence),
        keywords=keywords
    )

@router.get("/stats")
def get_stats():
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not initialized")
        
    try:
        # Aggregation
        total = db.reviews.count_documents({})
        
        # Sentiment Dist using Logic based on rating 
        # (This aligns with how we generated data: 1,2=Neg, 3=Neu, 4,5=Pos)
        pos = db.reviews.count_documents({"rating": {"$gt": 3}})
        neu = db.reviews.count_documents({"rating": 3})
        neg = db.reviews.count_documents({"rating": {"$lt": 3}})
        
        # Ratings Dist
        pipeline = [
            {"$group": {"_id": "$rating", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]
        ratings_data = list(db.reviews.aggregate(pipeline))
        # Format for chart [1star, 2star, ...]
        ratings_map = {r['_id']: r['count'] for r in ratings_data}
        ratings_dist = [ratings_map.get(i, 0) for i in [1.0, 2.0, 3.0, 4.0, 5.0]]
        
        # Top Words (this is heavy, returning mock or pre-calculated is better)
        # We will return mock top words for speed as calculating WC on 100k docs is slow in real-time
        top_words = [
            {"text": "great", "value": 1200},
            {"text": "good", "value": 900},
            {"text": "quality", "value": 850},
            {"text": "average", "value": 400},
            {"text": "okay", "value": 350},
            {"text": "product", "value": 800},
            {"text": "love", "value": 750},
            {"text": "fast", "value": 600},
            {"text": "shipping", "value": 550},
            {"text": "price", "value": 500},
            {"text": "bad", "value": 300},
            {"text": "excellent", "value": 450},
            {"text": "poor", "value": 250},
            {"text": "service", "value": 480},
            {"text": "recommend", "value": 700},
            {"text": "worth", "value": 420},
            {"text": "money", "value": 410},
            {"text": "cheap", "value": 380},
            {"text": "best", "value": 650},
            {"text": "happy", "value": 620},
            {"text": "broken", "value": 200},
            {"text": "perfect", "value": 580},
            {"text": "return", "value": 320},
            {"text": "small", "value": 280},
            {"text": "easy", "value": 520}
        ]
        
        return {
            "positive": pos,
            "neutral": neu,
            "negative": neg,
            "ratings_dist": ratings_dist,
            "top_words": top_words
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
