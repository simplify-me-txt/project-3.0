FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
# Install gcc for building python packages if needed
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 8000

# Run
CMD ["python", "backend/main.py"]
