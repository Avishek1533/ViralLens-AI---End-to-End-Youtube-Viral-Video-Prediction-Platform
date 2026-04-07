# ViralLens AI - Quick Start Guide

## Overview

ViralLens AI is a FastAPI application that predicts whether a YouTube video will go viral using machine learning models. Choose from 4 different models and get instant predictions based on video metadata.

## ⚡ Quick Start (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Server

**On Windows:**
```bash
run_server.bat
```

**On Linux/Mac:**
```bash
bash run_server.sh
```

**Or manually:**
```bash
uvicorn main:app --reload
```

### Step 3: Test the API
Open your browser to: http://localhost:8000/docs

### Step 4: Make a Prediction
Using Python:
```python
import requests

response = requests.post("http://localhost:8000/predict", json={
    "title": "Top 10 Most Shocking YouTube Moments!!!",
    "description": "Check this out! #viral #trending",
    "model": "random_forest"
})

result = response.json()
print(f"Trending: {result['is_trending']}")
print(f"Probability: {result['probability']:.1%}")
```

## 📁 Project Structure

```
ViralLens-AI/
├── main.py                                  # FastAPI application
├── requirements.txt                         # Python dependencies
├── logistic_regression_pipeline.joblib     # Trained model
├── random_forest_pipeline.joblib           # Trained model
├── xgboost_pipeline.joblib                 # Trained model
├── viral_prediction_dnn.joblib             # Trained model
├── example_usage.py                        # Python examples
├── run_server.sh / run_server.bat          # Server startup scripts
├── run_examples.sh / run_examples.bat      # Example runner scripts
├── CURL_EXAMPLES.md                        # cURL command examples
├── Dockerfile                              # Docker configuration
├── docker-compose.yml                      # Docker Compose setup
├── API_GUIDE.md                            # Comprehensive API documentation
└── README.md                               # Project information
```

## 🚀 Option A: Direct Python (Easiest)

### Windows
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start server
run_server.bat

# 3. In another terminal, run examples
run_examples.bat
```

### Linux/Mac
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start server
bash run_server.sh

# 3. In another terminal, run examples
bash run_examples.sh
```

## 🐳 Option B: Docker (Recommended for Production)

### Using Docker Compose (Simplest)
```bash
docker-compose up
```

Then access:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Using Docker directly
```bash
# Build
docker build -t virallens-ai .

# Run
docker run -p 8000:8000 virallens-ai
```

## 🌐 API Usage

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Make a Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Amazing Video Title!!!",
    "description": "Check this out! Subscribe for more!",
    "model": "random_forest"
  }'
```

### 3. Interactive API Documentation
Visit: http://localhost:8000/docs

Use the Swagger UI to test all endpoints interactively.

## 📊 Available Models

| Model | Speed | Accuracy | Best For |
|-------|-------|----------|----------|
| **Logistic Regression** | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | Baseline, quick predictions |
| **Random Forest** | ⚡⚡ Fast | ⭐⭐⭐⭐ Great | **Recommended** - balanced |
| **XGBoost** | ⚡ Slower | ⭐⭐⭐⭐⭐ Excellent | Maximum accuracy |
| **DNN** | ⚡ Slower | ⭐⭐⭐⭐ Great | Complex patterns |

## 🎯 Request Parameters

### Required
- **title** (string): Video title

### Optional
- **description** (string): Video description
- **tags** (string): Tags separated by `|`
- **view_count** (int): Expected views (default: 100,000)
- **likes** (int): Expected likes (default: 5,000)
- **comment_count** (int): Expected comments (default: 1,000)
- **category_id** (int): YouTube category (default: 24)
- **publish_hour** (int): Hour of publication 0-23 (default: 12)
- **publish_dow** (int): Day of week 0-6 (default: 3)
- **model** (string): Model choice (default: "random_forest")

## 📤 Response Format

```json
{
  "is_trending": true,
  "probability": 0.87,
  "model_used": "random_forest",
  "confidence": 0.87,
  "features_used": {
    "title": "Amazing Video Title!!!",
    "num_features": 26,
    "key_metrics": {
      "title_sentiment": 0.34,
      "engagement_ratio": 0.056,
      "hashtag_count": 3,
      "video_category": 24
    }
  }
}
```

## 🎮 Examples

### Python
```python
import requests

# Single prediction
url = "http://localhost:8000/predict"
payload = {
    "title": "Top 10 YouTube Fails",
    "likes": 5000,
    "view_count": 100000,
    "model": "random_forest"
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Trending: {result['is_trending']}")
print(f"Probability: {result['probability']:.1%}")
```

### JavaScript
```javascript
const payload = {
    title: "Top 10 YouTube Fails",
    likes: 5000,
    view_count: 100000,
    model: "random_forest"
};

fetch('http://localhost:8000/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
})
.then(r => r.json())
.then(d => console.log(`Trending: ${d.is_trending}`));
```

### cURL
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"title":"Top 10 YouTube Fails","model":"random_forest"}'
```

## 📋 YouTube Category IDs

| ID | Category |
|----|----------|
| 10 | Music |
| 15 | Pets & Animals |
| 17 | Sports |
| 20 | Gaming |
| 22 | People & Blogs |
| 23 | Comedy |
| 24 | Entertainment |
| 25 | News & Politics |
| 26 | How-to & Style |
| 27 | Education |
| 28 | Science & Technology |

## 🔧 Troubleshooting

### "No models loaded"
- Verify `.joblib` files are in the same directory as `main.py`
- Check file permissions
- Run `/health` endpoint to check status

### "Connection refused"
- Make sure server is running on port 8000
- Check if another application is using port 8000
- Try `lsof -i :8000` (Linux/Mac) or `netstat -ano | findstr :8000` (Windows)

### "Module not found"
- Run `pip install -r requirements.txt`
- Ensure you're using correct Python environment

### "Slow predictions"
- Use Random Forest or Logistic Regression for faster results
- Increase number of workers: `--workers 4`
- Check system resources

## 📚 Documentation

- **API_GUIDE.md**: Comprehensive API documentation with all endpoints
- **CURL_EXAMPLES.md**: Ready-to-use cURL commands
- **example_usage.py**: Python script with 7 usage examples
- **http://localhost:8000/docs**: Interactive Swagger UI

## 🚀 Production Deployment

### Using Gunicorn + Uvicorn
```bash
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Using Docker Compose
```bash
docker-compose up -d
```

Access: http://localhost:8000

## 📞 Support

- API Documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Check API_GUIDE.md for detailed information
- Review example_usage.py for code examples

## ✅ Checklist

- [ ] Installed requirements: `pip install -r requirements.txt`
- [ ] Models in correct directory
- [ ] Started server: `run_server.bat` or `bash run_server.sh`
- [ ] Tested health endpoint: `curl http://localhost:8000/health`
- [ ] Accessed Swagger UI: http://localhost:8000/docs
- [ ] Made first prediction

## 🎉 You're Ready!

Your ViralLens AI API is now running and ready to predict viral videos!

### Next Steps
1. Visit http://localhost:8000/docs for interactive testing
2. Review example_usage.py for code examples
3. Read API_GUIDE.md for comprehensive documentation
4. Deploy using Docker in production

---

**Need help?** Check the documentation files or run the examples:

**Windows:**
```bash
run_examples.bat
```

**Linux/Mac:**
```bash
bash run_examples.sh
```
