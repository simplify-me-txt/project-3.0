from datasets import load_dataset
import json
import tqdm
from datetime import datetime
import os
import random

# Target file
OUTPUT_FILE = "data/reviews_100k.json"
TARGET_COUNT = 100000

def download_and_process():
    print("Loading amazon_polarity dataset from Hugging Face...")
    
    try:
        # amazon_polarity is safe and doesn't require trust_remote_code
        dataset = load_dataset("amazon_polarity", split="train", streaming=True)
        
        reviews = []
        count = 0
        
        print("Extracting 100k reviews...")
        for data in tqdm.tqdm(dataset, total=TARGET_COUNT):
            if count >= TARGET_COUNT:
                break
            
            try:
                # amazon_polarity keys: label, title, content
                # label: 0 (negative), 1 (positive)
                
                label = data['label']
                
                # Heuristic to create 3 classes from binary dataset
                # 0: Negative, 1: Positive
                # We will randomly assign ~10-15% as Neutral (Rating 3)
                
                rand_val = random.random()
                
                if rand_val < 0.15:
                    # Synthesize Neutral
                    rating = 3.0
                    sentiment_label = "Neutral"
                else:
                    if label == 0:
                        rating = random.choice([1.0, 2.0])
                        sentiment_label = "Negative"
                    else:
                        rating = random.choice([4.0, 5.0])
                        sentiment_label = "Positive"
                
                title = data.get('title', '')
                content = data.get('content', '')
                full_text = f"{title}\n{content}" if title else content
                
                processed_review = {
                    'username': f"user_{random.randint(10000, 99999)}",
                    'product_name': "General Amazon Product",
                    'category': "General",
                    'review_text': full_text,
                    'rating': rating,
                    # We store the heuristic sentiment label for reference, 
                    # though ML will relearn this based on rating/text
                    'sentiment': sentiment_label, 
                    'timestamp': datetime.now().isoformat()
                }
                
                reviews.append(processed_review)
                count += 1
            except Exception as e:
                continue

        # Save to JSON
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(reviews, f, indent=2)
            
        print(f"Successfully saved {len(reviews)} reviews to {OUTPUT_FILE}")

    except Exception as e:
        print(f"Error downloading dataset: {e}")

if __name__ == "__main__":
    if not os.path.exists('data'):
        os.makedirs('data')
    download_and_process()
