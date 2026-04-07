# ViralLens AI - FastAPI Application

A FastAPI application for predicting whether a YouTube video will go viral using machine learning models.

## Features

- **Multiple Models**: Choose between Logistic Regression, Random Forest, XGBoost, and Deep Neural Network
- **Smart Feature Extraction**: Automatically extracts 26+ features from video metadata
- **Batch Predictions**: Support for batch processing up to 100 videos at once
- **Interactive Documentation**: Auto-generated Swagger UI and ReDoc documentation
- **Comprehensive Analysis**: Provides prediction probability and confidence scores
- **Sentiment Analysis**: Uses VADER sentiment analyzer for title/description analysis

## Installation

### 1. Extract Models
Ensure the following joblib files are in the same directory as `main.py`:
- `logistic_regression_pipeline.joblib`
- `random_forest_pipeline.joblib`
- `xgboost_pipeline.joblib`
- `viral_prediction_dnn.joblib`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Option 1: Using Uvicorn (Development)
```bash
python main.py
```

Or directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Using Uvicorn (Production)
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Option 3: Using Docker
```bash
docker build -t virallens-ai .
docker run -p 8000:8000 virallens-ai
```

## API Endpoints

### 1. Health Check
```
GET /health
```
Check if all models are loaded and healthy.

**Response:**
```json
{
  "status": "healthy",
  "loaded_models": ["random_forest", "xgboost", "logistic_regression", "dnn"],
  "message": "4 models loaded successfully"
}
```

---

### 2. Single Prediction
```
POST /predict
```

Predict if a single video will be trending.

**Request Body:**
```json
{
  "title": "Top 10 Most Shocking YouTube Moments!",
  "description": "Watch the most shocking moments on YouTube. Subscribe for more! #YouTube #Shocking",
  "tags": "YouTube|Shocking|Moments|Trending",
  "view_count": 500000,
  "likes": 25000,
  "comment_count": 5000,
  "category_id": 24,
  "publish_hour": 18,
  "publish_dow": 5,
  "model": "random_forest"
}
```

**Response:**
```json
{
  "is_trending": true,
  "probability": 0.87,
  "model_used": "random_forest",
  "confidence": 0.87,
  "features_used": {
    "title": "Top 10 Most Shocking YouTube Moments!",
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

---

### 3. Batch Predictions
```
POST /predict-batch
```

Predict for multiple videos at once (max 100).

**Request Body:**
```json
[
  {
    "title": "Video 1 Title",
    "description": "Description 1",
    "model": "random_forest"
  },
  {
    "title": "Video 2 Title",
    "description": "Description 2",
    "model": "xgboost"
  }
]
```

**Response:**
```json
{
  "total_videos": 2,
  "successful": 2,
  "results": [
    {
      "is_trending": true,
      "probability": 0.82,
      "model_used": "random_forest",
      "confidence": 0.82,
      "features_used": {...}
    },
    {
      "is_trending": false,
      "probability": 0.35,
      "model_used": "xgboost",
      "confidence": 0.65,
      "features_used": {...}
    }
  ]
}
```

---

### 4. List Available Models
```
GET /models
```

Get information about all available models.

**Response:**
```json
{
  "available_models": {
    "logistic_regression": {
      "path": ".../logistic_regression_pipeline.joblib",
      "exists": true,
      "loaded": true,
      "description": "Linear model for binary classification"
    },
    "random_forest": {
      "path": ".../random_forest_pipeline.joblib",
      "exists": true,
      "loaded": true,
      "description": "Ensemble tree-based model (recommended)"
    },
    ...
  }
}
```

---

### 5. Feature Information
```
GET /features-info
```

Get detailed information about all features used in predictions.

---

### 6. Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Feature Explanations

### Title Features
- `title_length`: Character length of video title
- `title_word_count`: Number of words in title
- `title_has_question`: Whether title contains a question mark
- `title_has_exclaim`: Whether title contains an exclamation mark
- `title_num_caps_words`: Number of capitalized words
- `title_has_number`: Whether title contains numbers
- `title_sentiment`: VADER sentiment score (-1 to 1)

### Description Features
- `description_length`: Character length of description
- `description_wc`: Word count in description
- `hashtag_count`: Number of hashtags
- `link_count`: Number of links
- `desc_has_social`: Whether description mentions social media
- `desc_emoji_count`: Number of emojis

### Engagement Features
- `like_ratio`: Likes divided by view count
- `comment_ratio`: Comments divided by view count
- `engagement`: Sum of engagement ratios

### Temporal Features
- `publish_hour`: Hour of day (0-23) when video was published
- `publish_dow`: Day of week (0=Monday, 6=Sunday)
- `is_weekend`: Whether published on weekend

### Metadata
- `category_id`: YouTube category ID
- `tag_count`: Number of tags

## Model Descriptions

### Logistic Regression
- Simple, interpretable linear model
- Fast inference
- Good baseline for binary classification

### Random Forest (Recommended)
- Ensemble of decision trees
- Captures non-linear patterns
- Robust to outliers
- **Default model**

### XGBoost
- Gradient boosting model
- High accuracy and performance
- Best for complex interactions
- Slower training but reliable predictions

### Deep Neural Network (DNN)
- Neural network architecture
- Can capture complex patterns
- Best with diverse feature inputs
- Useful for exploring non-linear relationships

## Example Usage

### Using cURL
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "This Will Go Viral!!!",
    "description": "Check this out #trending #viral",
    "likes": 10000,
    "comment_count": 2000,
    "view_count": 500000,
    "model": "random_forest"
  }'
```

### Using Python Requests
```python
import requests

url = "http://localhost:8000/predict"
payload = {
    "title": "This Will Go Viral!!!",
    "description": "Check this out #trending #viral",
    "likes": 10000,
    "comment_count": 2000,
    "view_count": 500000,
    "model": "random_forest"
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Trending: {result['is_trending']}")
print(f"Probability: {result['probability']:.2%}")
print(f"Confidence: {result['confidence']:.2%}")
```

### Using JavaScript/Fetch
```javascript
const payload = {
    title: "This Will Go Viral!!!",
    description: "Check this out #trending #viral",
    likes: 10000,
    comment_count: 2000,
    view_count: 500000,
    model: "random_forest"
};

fetch('http://localhost:8000/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
})
.then(response => response.json())
.then(data => {
    console.log(`Trending: ${data.is_trending}`);
    console.log(`Probability: ${(data.probability * 100).toFixed(2)}%`);
    console.log(`Confidence: ${(data.confidence * 100).toFixed(2)}%`);
});
```

## Default Parameter Values

When parameters are not provided, the API uses these defaults:

| Parameter | Default | Range |
|-----------|---------|-------|
| `view_count` | 100,000 | > 0 |
| `likes` | 5,000 | >= 0 |
| `comment_count` | 1,000 | >= 0 |
| `category_id` | 24 | 1-29 |
| `publish_hour` | 12 | 0-23 |
| `publish_dow` | 3 | 0-6 |
| `model` | random_forest | See models |

## YouTube Category IDs

| ID | Category |
|----|----------|
| 1 | Film & Animation |
| 2 | Autos & Vehicles |
| 10 | Music |
| 15 | Pets & Animals |
| 17 | Sports |
| 18 | Short Movies |
| 19 | Travel & Events |
| 20 | Gaming |
| 22 | People & Blogs |
| 23 | Comedy |
| 24 | Entertainment |
| 25 | News & Politics |
| 26 | How-to & Style |
| 27 | Education |
| 28 | Science & Technology |
| 29 | Nonprofits & Activism |

## Notes

- The application requires all 4 model files to be present for full functionality
- Predictions are based on features extracted from titles, descriptions, and engagement metrics
- For best results, provide accurate engagement metrics and metadata
- The "viral" threshold is based on the 90th percentile of view counts in the training data

## Troubleshooting

### Models not loading
- Verify all `.joblib` files are in the same directory as `main.py`
- Check file permissions
- Run health check: `GET /health`

### Prediction errors
- Ensure all required fields are provided
- Check that `publish_hour` is 0-23
- Verify `publish_dow` is 0-6
- Confirm `category_id` is valid (1-29)

### Performance issues
- Use the batch endpoint instead of multiple single predictions
- Consider using Random Forest or Logistic Regression for faster inference
- Increase number of workers: `--workers 4` (or more)

## License

See LICENSE file

## Author

ViralLens AI Development Team

## Support

For issues or questions, please refer to the project documentation or contact support.
