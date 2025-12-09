import requests
import gzip
import json
import pandas as pd
import os
from datetime import datetime
import tqdm

# URL for Amazon Cell Phones & Accessories Reviews (5-core, substantial size)
DATA_URL = "http://deepyeti.ucsd.edu/jianmo/amazon/categoryFilesSmall/Cell_Phones_and_Accessories_5.json.gz"
OUTPUT_FILE = "data/reviews_100k.json"
TARGET_COUNT = 100000

def download_and_process():
    print(f"Downloading dataset from {DATA_URL}...")
    
    # stream download to process on the fly without saving huge temp file if possible, 
    # but requests+gzip is tricky. Better to save to temp file.
    local_filename = "data/temp_data.json.gz"
    
    if not os.path.exists('data'):
        os.makedirs('data')

    # Download with progress bar
    response = requests.get(DATA_URL, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    
    with open(local_filename, 'wb') as f, tqdm.tqdm(
        desc="Downloading",
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(block_size):
            size = f.write(data)
            bar.update(size)
            
    print("Download complete. Processing and extracting 100k reviews...")
    
    reviews = []
    count = 0
    
    with gzip.open(local_filename, 'rt', encoding='utf-8') as f:
        for line in tqdm.tqdm(f, total=TARGET_COUNT, desc="Processing"):
            if count >= TARGET_COUNT:
                break
            
            try:
                data = json.loads(line)
                
                # Check for required fields
                if 'reviewText' not in data or 'overall' not in data:
                    continue
                    
                processed_review = {
                    'username': data.get('reviewerName', 'Anonymous'),
                    'product_name': data.get('asin', 'Unknown Product'), # using asin as name for now
                    'category': 'Cell Phones & Accessories',
                    'review_text': data['reviewText'],
                    'rating': float(data['overall']),
                    'timestamp': datetime.fromtimestamp(data.get('unixReviewTime', 0)).isoformat()
                }
                reviews.append(processed_review)
                count += 1
            except Exception as e:
                continue

    # Save to JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, indent=2)
        
    print(f"Successfully saved {len(reviews)} reviews to {OUTPUT_FILE}")
    
    # Cleanup
    if os.path.exists(local_filename):
        os.remove(local_filename)

if __name__ == "__main__":
    download_and_process()
