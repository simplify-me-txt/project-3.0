from fastapi import APIRouter, Query, HTTPException
from backend.database import get_database
from typing import Optional, List
from pydantic import BaseModel

router = APIRouter()

class Review(BaseModel):
    product_name: str
    category: str
    review_text: str
    rating: float
    sentiment: Optional[str] = None
    timestamp: str

class ReviewResponse(BaseModel):
    reviews: List[Review]
    total: int

@router.get("/", response_model=ReviewResponse)
def get_reviews(
    search: Optional[str] = None,
    sentiment: Optional[str] = None,
    rating: Optional[float] = None,
    skip: int = 0,
    limit: int = 20
):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not initialized")
        
    query = {}
    
    if search:
        query["review_text"] = {"$regex": search, "$options": "i"}
        
    if sentiment:
        if sentiment.lower() == "positive":
            query["rating"] = {"$gt": 3}
        elif sentiment.lower() == "neutral":
             query["rating"] = 3
        elif sentiment.lower() == "negative":
            query["rating"] = {"$lt": 3}
            
    if rating:
        query["rating"] = rating
        
    try:
        total = db.reviews.count_documents(query)
        cursor = db.reviews.find(query).skip(skip).limit(limit)
        reviews = []
        for doc in cursor:
            # Map doc to model
            r = doc['rating']
            if r > 3: sent = "Positive"
            elif r == 3: sent = "Neutral"
            else: sent = "Negative"
            
            doc['sentiment'] = sent
            reviews.append(doc)
            
        return {"reviews": reviews, "total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=dict)
def add_review(review: Review):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not initialized")
    
    try:
        review_dict = review.dict()
        # Ensure timestamp is set if missing? Model requires it so it's fine.
        result = db.reviews.insert_one(review_dict)
        return {"id": str(result.inserted_id), "message": "Review added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
