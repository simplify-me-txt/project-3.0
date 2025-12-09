from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.database import connect_to_mongo, close_mongo_connection
from backend.routes import reviews, sentiment
import os

app = FastAPI(title="E-Commerce Sentiment Analysis API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Connection Events
@app.on_event("startup")
def startup_db_client():
    connect_to_mongo()
    # Preload model
    sentiment.load_model()

@app.on_event("shutdown")
def shutdown_db_client():
    close_mongo_connection()

# Routes
app.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
app.include_router(sentiment.router, prefix="", tags=["sentiment"])

# Mount Frontend (Static Files)
# Ensure frontend directory exists relative to execution path
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
else:
    print("Frontend directory not found. Running in API-only mode.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8100, reload=True)
