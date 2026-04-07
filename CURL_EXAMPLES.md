# ViralLens AI - cURL Examples for API Testing

## 1. Health Check
curl -X GET http://localhost:8000/health


## 2. Single Prediction - Basic
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Top 10 Most Shocking YouTube Moments!",
    "description": "Watch amazing moments on YouTube. Subscribe!",
    "model": "random_forest"
  }'


## 3. Single Prediction - Full Parameters
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "THIS WILL BLOW YOUR MIND!!!",
    "description": "Check out this incredible discovery! #viral #trending #amazing",
    "tags": "viral|trending|amazing|youtube|wow",
    "view_count": 500000,
    "likes": 25000,
    "comment_count": 5000,
    "category_id": 24,
    "publish_hour": 18,
    "publish_dow": 5,
    "model": "random_forest"
  }'


## 4. Compare Models
# Logistic Regression
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Python in 10 Minutes",
    "model": "logistic_regression"
  }'

# Random Forest
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Python in 10 Minutes",
    "model": "random_forest"
  }'

# XGBoost
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Python in 10 Minutes",
    "model": "xgboost"
  }'

# DNN
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Python in 10 Minutes",
    "model": "dnn"
  }'


## 5. Batch Prediction
curl -X POST http://localhost:8000/predict-batch \
  -H "Content-Type: application/json" \
  -d '[
    {
      "title": "Gaming Stream - Fortnite",
      "description": "High-level gaming content",
      "model": "random_forest"
    },
    {
      "title": "DIY Home Renovation",
      "description": "Budget-friendly home improvement tips",
      "model": "xgboost"
    },
    {
      "title": "Cute Puppies Playing",
      "description": "The cutest puppies ever!",
      "model": "random_forest"
    }
  ]'


## 6. List Available Models
curl -X GET http://localhost:8000/models


## 7. Get Features Information
curl -X GET http://localhost:8000/features-info


## 8. Pretty Print JSON Response
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Amazing Video Title",
    "model": "random_forest"
  }' | python -m json.tool


## 9. Save Response to File
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Amazing Video Title",
    "model": "random_forest"
  }' -o prediction_result.json


## 10. Test with Different Engagement Levels
# Low engagement
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Video",
    "view_count": 1000,
    "likes": 20,
    "comment_count": 5,
    "model": "random_forest"
  }'

# High engagement
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Video",
    "view_count": 1000000,
    "likes": 80000,
    "comment_count": 20000,
    "model": "random_forest"
  }'


## 11. Test All Categories
# 10 - Music
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"title":"Amazing Music Video","category_id": 10,"model":"random_forest"}'

# 20 - Gaming
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"title":"Gameplay Highlights","category_id": 20,"model":"random_forest"}'

# 27 - Education
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"title":"Learn Something New","category_id": 27,"model":"random_forest"}'


## 12. Test Different Publishing Times
# Early morning (6 AM)
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"title":"Morning Video","publish_hour": 6,"model":"random_forest"}'

# Peak hours (6 PM)
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"title":"Peak Hours Video","publish_hour": 18,"model":"random_forest"}'

# Night time (11 PM)
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"title":"Night Video","publish_hour": 23,"model":"random_forest"}'


## 13. Test Different Days of Week
# Monday (0)
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"title":"Monday Video","publish_dow": 0,"model":"random_forest"}'

# Friday (4)
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"title":"Friday Video","publish_dow": 4,"model":"random_forest"}'

# Weekend (5 = Saturday)
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"title":"Weekend Video","publish_dow": 5,"model":"random_forest"}'
