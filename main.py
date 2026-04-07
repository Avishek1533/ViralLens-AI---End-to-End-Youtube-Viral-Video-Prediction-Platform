"""
ViralLens AI - FastAPI Application for YouTube Viral Video Prediction
Provides endpoints to predict if a video will be trending using multiple ML/DNN models.
"""

import os
import re
import joblib
from datetime import datetime
from typing import Optional, Literal
import numpy as np
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize FastAPI app
app = FastAPI(
    title="ViralLens AI - YouTube Viral Video Prediction",
    description="Predict if a YouTube video will go viral using ML models",
    version="1.0.0"
)

# Model paths
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS = {
    "logistic_regression": os.path.join(MODEL_DIR, "logistic_regression_pipeline.joblib"),
    "random_forest": os.path.join(MODEL_DIR, "random_forest_pipeline.joblib"),
    "xgboost": os.path.join(MODEL_DIR, "xgboost_pipeline.joblib"),
    "dnn": os.path.join(MODEL_DIR, "viral_prediction_dnn.joblib"),
}

# Load models at startup
loaded_models = {}
try:
    for model_name, model_path in MODELS.items():
        if os.path.exists(model_path):
            loaded_models[model_name] = joblib.load(model_path)
            print(f"✓ Loaded {model_name} model")
        else:
            print(f"✗ {model_name} model not found at {model_path}")
except Exception as e:
    print(f"Error loading models: {e}")

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Regular expressions for text processing
EMOJI_RE = re.compile('['
    u'\U0001F600-\U0001FFFF'
    u'\U00002702-\U000027B0'
    u'\U000024C2-\U0001F251'
    ']+', flags=re.UNICODE)

URL_RE = re.compile(r'http\S+|www\.\S+', re.IGNORECASE)


# ─────────────────────────────────────────────────────────────────────────────
# Pydantic Models for Request/Response
# ─────────────────────────────────────────────────────────────────────────────

class VideoFeatures(BaseModel):
    """Video features for prediction"""
    title: str = Field(..., description="Video title", min_length=1)
    description: Optional[str] = Field("", description="Video description")
    tags: Optional[str] = Field("", description="Video tags (separated by |)")
    
    # Engagement metrics (optional - use defaults if not provided)
    view_count: Optional[int] = Field(100000, description="View count")
    likes: Optional[int] = Field(5000, description="Number of likes")
    comment_count: Optional[int] = Field(1000, description="Number of comments")
    
    # Metadata
    category_id: Optional[int] = Field(24, description="YouTube category ID (default: Entertainment)")
    publish_hour: Optional[int] = Field(12, description="Hour of publication (0-23)")
    publish_dow: Optional[int] = Field(3, description="Day of week (0=Monday, 6=Sunday)")
    
    # Model selection
    model: Literal["logistic_regression", "random_forest", "xgboost", "dnn"] = Field(
        "random_forest", 
        description="Select prediction model"
    )


class PredictionResponse(BaseModel):
    """Prediction result"""
    is_trending: bool = Field(..., description="Whether video is predicted to be trending")
    probability: float = Field(..., description="Probability of being viral (0-1)")
    model_used: str = Field(..., description="Model used for prediction")
    confidence: float = Field(..., description="Confidence score")
    features_used: dict = Field(..., description="Features used in prediction")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    loaded_models: list
    message: str


# ─────────────────────────────────────────────────────────────────────────────
# Feature Engineering Functions
# ─────────────────────────────────────────────────────────────────────────────

def normalize_text(text: str) -> str:
    """Normalize text by removing URLs, emojis, and extra whitespace"""
    if not isinstance(text, str):
        return ''
    text = text.lower()
    text = URL_RE.sub('', text)
    text = EMOJI_RE.sub('', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_title_features(title: str) -> dict:
    """Extract features from video title"""
    title_clean = normalize_text(title)
    
    features = {
        'title_length': len(title_clean),
        'title_word_count': len(title_clean.split()),
        'title_char_count': len(title),
        'title_has_question': 1 if '?' in title else 0,
        'title_has_exclaim': 1 if '!' in title else 0,
        'title_num_caps_words': sum(1 for w in title.split() if w.isupper() and len(w) > 1),
        'title_has_number': 1 if re.search(r'\d', title_clean) else 0,
        'title_keyword_count': len(title_clean.split()),
        'title_sentiment': sia.polarity_scores(title_clean)['compound'],
    }
    return features


def extract_description_features(description: str) -> dict:
    """Extract features from video description"""
    description_clean = normalize_text(description)
    
    features = {
        'description_length': len(description_clean),
        'description_wc': len(description_clean.split()),
        'hashtag_count': len(re.findall(r'#\w+', description)),
        'link_count': len(re.findall(r'https?://', description)),
        'desc_has_social': 1 if re.search(r'instagram|twitter|facebook|tiktok', description, re.IGNORECASE) else 0,
        'desc_emoji_count': len(EMOJI_RE.findall(description)),
    }
    return features


def extract_tag_features(tags: str) -> dict:
    """Extract features from video tags"""
    tag_count = len([t for t in tags.split('|') if t.strip()]) if tags else 0
    
    return {
        'tag_count': tag_count,
    }


def extract_engagement_features(view_count: int, likes: int, comment_count: int) -> dict:
    """Extract engagement ratio features"""
    EPS = 1e-8
    
    like_ratio = likes / (view_count + EPS)
    comment_ratio = comment_count / (view_count + EPS)
    engagement = like_ratio + comment_ratio
    
    return {
        'view_count': view_count,
        'likes': likes,
        'comment_count': comment_count,
        'like_ratio': like_ratio,
        'comment_ratio': comment_ratio,
        'engagement': engagement,
    }


def extract_temporal_features(
    publish_hour: int = 12,
    publish_dow: int = 3,
) -> dict:
    """Extract temporal features"""
    
    return {
        'publish_hour': publish_hour,
        'publish_dow': publish_dow,
        'is_weekend': 1 if publish_dow >= 5 else 0,
        'days_to_trend': 0,  # Default: assume immediate
    }


def prepare_features(video_data: VideoFeatures) -> tuple[dict, np.ndarray]:
    """
    Prepare all features for model prediction
    Returns: (feature_dict, feature_array)
    """
    # Extract all feature groups
    title_features = extract_title_features(video_data.title)
    desc_features = extract_description_features(video_data.description)
    tag_features = extract_tag_features(video_data.tags)
    engagement_features = extract_engagement_features(
        video_data.view_count, 
        video_data.likes, 
        video_data.comment_count
    )
    temporal_features = extract_temporal_features(
        video_data.publish_hour,
        video_data.publish_dow
    )
    
    # Combine all features
    all_features = {
        **title_features,
        **desc_features,
        **tag_features,
        **engagement_features,
        **temporal_features,
        'categoryId': video_data.category_id,
    }
    
    # Create feature array in the order expected by models
    # This should match the order used during training
    feature_order = [
        'title_length', 'title_word_count', 'title_char_count',
        'title_has_question', 'title_has_exclaim', 'title_num_caps_words',
        'title_has_number', 'title_keyword_count', 'title_sentiment',
        'description_length', 'description_wc', 'hashtag_count',
        'link_count', 'desc_has_social', 'desc_emoji_count',
        'tag_count', 'view_count', 'likes', 'comment_count',
        'like_ratio', 'comment_ratio', 'engagement',
        'publish_hour', 'publish_dow', 'is_weekend',
        'days_to_trend', 'categoryId',
    ]
    
    feature_array = np.array([all_features.get(feat, 0) for feat in feature_order]).reshape(1, -1)
    
    return all_features, feature_array


# ─────────────────────────────────────────────────────────────────────────────
# API Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Info"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "ViralLens AI - YouTube Viral Video Prediction",
        "version": "1.0.0",
        "description": "Predict if a YouTube video will go viral using ML models",
        "docs": "/docs",
        "models_available": list(loaded_models.keys()),
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    if not loaded_models:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "loaded_models": [],
                "message": "No models loaded",
            }
        )
    
    return {
        "status": "healthy",
        "loaded_models": list(loaded_models.keys()),
        "message": f"{len(loaded_models)} models loaded successfully",
    }


@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
async def predict(video_data: VideoFeatures):
    """
    Predict if a video will be trending
    
    **Parameters:**
    - **title**: Video title (required)
    - **description**: Video description (optional)
    - **tags**: Tags separated by | (optional)
    - **view_count**: Expected view count (default: 100,000)
    - **likes**: Expected likes (default: 5,000)
    - **comment_count**: Expected comments (default: 1,000)
    - **category_id**: YouTube category ID (default: 24 - Entertainment)
    - **publish_hour**: Hour of publication 0-23 (default: 12)
    - **publish_dow**: Day of week 0-6 (default: 3 - Wednesday)
    - **model**: Model to use (default: random_forest)
    """
    
    # Check if model is loaded
    if video_data.model not in loaded_models:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{video_data.model}' not loaded. Available: {list(loaded_models.keys())}"
        )
    
    try:
        # Prepare features
        features_dict, features_array = prepare_features(video_data)
        
        # Get model
        model = loaded_models[video_data.model]
        
        # Make prediction
        prediction = model.predict(features_array)[0]
        
        # Get probability if available
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(features_array)[0]
            probability = float(probabilities[1]) if len(probabilities) > 1 else float(probabilities[0])
        else:
            probability = float(prediction)
        
        is_trending = bool(prediction == 1 or prediction > 0.5)
        confidence = max(probability, 1 - probability)
        
        return {
            "is_trending": is_trending,
            "probability": probability,
            "model_used": video_data.model,
            "confidence": confidence,
            "features_used": {
                "title": video_data.title[:50] + "..." if len(video_data.title) > 50 else video_data.title,
                "num_features": len(features_dict),
                "key_metrics": {
                    "title_sentiment": features_dict.get("title_sentiment", 0),
                    "engagement_ratio": features_dict.get("engagement", 0),
                    "hashtag_count": features_dict.get("hashtag_count", 0),
                    "video_category": video_data.category_id,
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )


@app.get("/models", tags=["Info"])
async def list_models():
    """List available models with details"""
    models_info = {}
    for model_name in MODELS.keys():
        model_path = MODELS[model_name]
        exists = os.path.exists(model_path)
        loaded = model_name in loaded_models
        
        models_info[model_name] = {
            "path": model_path,
            "exists": exists,
            "loaded": loaded,
            "description": {
                "logistic_regression": "Linear model for binary classification",
                "random_forest": "Ensemble tree-based model (recommended)",
                "xgboost": "Gradient boosting model with high accuracy",
                "dnn": "Deep Neural Network for complex patterns",
            }.get(model_name, ""),
        }
    
    return {"available_models": models_info}


@app.post("/predict-batch", tags=["Predictions"])
async def predict_batch(videos: list[VideoFeatures]):
    """
    Batch prediction for multiple videos
    Limited to 100 videos per request
    """
    if len(videos) > 100:
        raise HTTPException(
            status_code=400,
            detail="Batch size limited to 100 videos"
        )
    
    results = []
    for video in videos:
        try:
            result = await predict(video)
            results.append(result)
        except HTTPException as e:
            results.append({
                "error": e.detail,
                "title": video.title,
            })
    
    return {
        "total_videos": len(videos),
        "successful": len([r for r in results if "error" not in r]),
        "results": results,
    }


@app.get("/features-info", tags=["Info"])
async def features_info():
    """Get information about features used in predictions"""
    return {
        "title_features": {
            "title_length": "Character count of title",
            "title_word_count": "Number of words in title",
            "title_has_question": "Binary: contains question mark",
            "title_has_exclaim": "Binary: contains exclamation mark",
            "title_num_caps_words": "Number of capitalized words",
            "title_has_number": "Binary: contains numbers",
            "title_sentiment": "Sentiment score (-1 to 1)",
        },
        "description_features": {
            "description_length": "Character count of description",
            "description_wc": "Word count in description",
            "hashtag_count": "Number of hashtags",
            "link_count": "Number of links",
            "desc_has_social": "Binary: mentions social media",
            "desc_emoji_count": "Number of emojis",
        },
        "engagement_features": {
            "view_count": "Total views",
            "likes": "Number of likes",
            "comment_count": "Number of comments",
            "like_ratio": "Likes / Views",
            "comment_ratio": "Comments / Views",
            "engagement": "Sum of ratios",
        },
        "temporal_features": {
            "publish_hour": "Hour of day (0-23)",
            "publish_dow": "Day of week (0-6)",
            "is_weekend": "Binary: published on weekend",
        },
        "metadata_features": {
            "tag_count": "Number of tags",
            "categoryId": "YouTube category ID",
        },
    }


# ─────────────────────────────────────────────────────────────────────────────
# Error Handlers
# ─────────────────────────────────────────────────────────────────────────────

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": f"Invalid value: {str(exc)}"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
