# E-Commerce Reviews Sentiment Analysis

A Big Data Web Application that analyzes 200,000+ real-world e-commerce product reviews to predict sentiment, visualize trends, and provide deep insights using Machine Learning.

## Features

- **Big Data Handling**: Ingests and processes over 200,000 reviews (Amazon Polarity Dataset).
- **Sentiment Analysis**: Uses Logistic Regression (Accuracy ~92%) to classify reviews as Positive/Negative/Neutral in real-time.
- **Interactive Dashboard**: Visualizes sentiment distribution, ratings, and trends with a compact, modern layout.
- **Search & Filter API**: Efficiently query reviews by keyword, sentiment, and rating with advanced pagination.
- **Review Interaction**: Clickable review rows with detailed modal popups.
- **Save Feature**: Analyze custom text and save results directly to the database.
- **Premium UI**: Modern, glassmorphism-inspired design with Dark/Light mode and animated metrics.

## Tech Stack

- **Frontend**: Vanilla HTML5, CSS3, JavaScript (No frameworks), Chart.js
- **Backend**: Python FastAPI, Numpy, Scikit-learn
- **Database**: MongoDB
- **Data Source**: Hugging Face `amazon_polarity` dataset

## Prerequisites

- Python 3.9+
- MongoDB (Running on localhost:27017)

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd e-com-analysis
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download & Ingest Data**
   This downloads the dataset and populates MongoDB.
   ```bash
   # Download Data
   python data/download_hf_data.py
   
   # Ingest into MongoDB
   python data/ingest_data.py
   ```

4. **Train Models**
   Train the Sentiment Analysis model (saved to `backend/models`).
   ```bash
   python data/train_models.py
   ```

5. **Run the Application**
   Start the FastAPI backend (serves frontend at root).
   ```bash
   python backend/main.py
   ```
   
   Open [http://localhost:8100](http://localhost:8100) in your browser.

## Deployment (Docker)

To run with Docker Compose:

1. Build and Run
   ```bash
   docker-compose up --build
   ```

2. Access at `http://localhost:8100`.

## Project Structure

- `backend/`: FastAPI application and ML models.
- `frontend/`: HTML/CSS/JS files.
- `data/`: Data processing and training scripts.

