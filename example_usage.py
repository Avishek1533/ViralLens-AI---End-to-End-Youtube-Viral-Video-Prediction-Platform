"""
Example Python script demonstrating the ViralLens AI FastAPI application
"""

import requests
import json

# API base URL
API_URL = "http://localhost:8000"

# Example 1: Single Prediction
def example_single_prediction():
    """Make a single prediction for a video"""
    print("=" * 80)
    print("EXAMPLE 1: Single Video Prediction")
    print("=" * 80)
    
    payload = {
        "title": "Top 10 Most Shocking YouTube Moments That Will Blow Your Mind!",
        "description": """
        Watch the most shocking and unbelievable moments on YouTube. 
        From epic fails to incredible stunts - this video has it all!
        
        Subscribe for more amazing content! #YouTube #Shocking #Trending #Viral
        """,
        "tags": "YouTube|Shocking|Trending|Viral|Fail|Moments|Epic",
        "view_count": 500000,
        "likes": 25000,
        "comment_count": 5000,
        "category_id": 24,  # Entertainment
        "publish_hour": 18,  # 6 PM
        "publish_dow": 5,    # Friday
        "model": "random_forest"
    }
    
    try:
        response = requests.post(f"{API_URL}/predict", json=payload)
        response.raise_for_status()
        result = response.json()
        
        print(f"\nVideo Title: {payload['title']}")
        print(f"Model Used: {result['model_used']}")
        print(f"Prediction: {'VIRAL ✓' if result['is_trending'] else 'NOT VIRAL ✗'}")
        print(f"Probability: {result['probability']:.1%}")
        print(f"Confidence: {result['confidence']:.1%}")
        print(f"\nKey Metrics:")
        for key, value in result['features_used']['key_metrics'].items():
            print(f"  {key}: {value}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


# Example 2: Test Different Models
def example_compare_models():
    """Compare predictions across different models"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Compare All Models")
    print("=" * 80)
    
    video = {
        "title": "Learn Python Programming in 10 Minutes!",
        "description": "Quick tutorial on Python basics for beginners. Perfect for learning!",
        "tags": "Python|Programming|Tutorial|Learning|Coding",
        "view_count": 250000,
        "likes": 8000,
        "comment_count": 1500,
        "category_id": 27,  # Education
        "publish_hour": 14,
        "publish_dow": 2,   # Tuesday
    }
    
    models = ["logistic_regression", "random_forest", "xgboost", "dnn"]
    
    print(f"\nTitle: {video['title']}\n")
    print("Model Comparison:")
    print("-" * 80)
    print(f"{'Model':<25} {'Trending':<12} {'Probability':<15} {'Confidence':<15}")
    print("-" * 80)
    
    for model in models:
        payload = {**video, "model": model}
        try:
            response = requests.post(f"{API_URL}/predict", json=payload)
            result = response.json()
            
            print(f"{model:<25} {str(result['is_trending']):<12} "
                  f"{result['probability']:.1%}            {result['confidence']:.1%}")
            
        except requests.exceptions.RequestException as e:
            print(f"{model:<25} Error: {str(e)[:30]}")


# Example 3: Batch Prediction
def example_batch_prediction():
    """Make predictions for multiple videos at once"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Batch Prediction (Multiple Videos)")
    print("=" * 80)
    
    videos = [
        {
            "title": "Gaming Stream - Competitive Fortnite!",
            "description": "High-level Fortnite gaming. Watch pro players compete!",
            "tags": "Gaming|Fortnite|Streaming|Competitive",
            "view_count": 300000,
            "likes": 15000,
            "comment_count": 3000,
            "category_id": 20,  # Gaming
            "model": "random_forest"
        },
        {
            "title": "DIY Home Renovation - Budget Friendly Tips!",
            "description": "Learn how to renovate your home on a budget.",
            "tags": "DIY|Home|Renovation|Budget",
            "view_count": 150000,
            "likes": 5000,
            "comment_count": 800,
            "category_id": 26,  # How-to & Style
            "model": "xgboost"
        },
        {
            "title": "Cute Puppies Playing - Most Adorable Moments",
            "description": "The cutest puppies playing and having fun. Pure joy!",
            "tags": "Puppies|Cute|Animals|Pets",
            "view_count": 800000,
            "likes": 40000,
            "comment_count": 10000,
            "category_id": 15,  # Pets & Animals
            "model": "random_forest"
        },
    ]
    
    try:
        response = requests.post(f"{API_URL}/predict-batch", json=videos)
        response.raise_for_status()
        result = response.json()
        
        print(f"\nProcessed {result['total_videos']} videos")
        print(f"Successful predictions: {result['successful']}")
        print("\nResults:")
        print("-" * 80)
        
        for i, video_result in enumerate(result['results'], 1):
            if 'error' not in video_result:
                print(f"\n{i}. Title: {videos[i-1]['title']}")
                print(f"   Model: {video_result['model_used']}")
                print(f"   Trending: {'YES ✓' if video_result['is_trending'] else 'NO ✗'}")
                print(f"   Probability: {video_result['probability']:.1%}")
            else:
                print(f"\n{i}. Error: {video_result['error']}")
                
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


# Example 4: Check API Health
def example_health_check():
    """Check if API and models are healthy"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: API Health Check")
    print("=" * 80)
    
    try:
        response = requests.get(f"{API_URL}/health")
        response.raise_for_status()
        health = response.json()
        
        print(f"\nStatus: {health['status'].upper()}")
        print(f"Message: {health['message']}")
        print(f"\nLoaded Models:")
        for model in health['loaded_models']:
            print(f"  ✓ {model}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


# Example 5: Get Available Models Info
def example_models_info():
    """Get information about all available models"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Available Models Information")
    print("=" * 80)
    
    try:
        response = requests.get(f"{API_URL}/models")
        response.raise_for_status()
        models = response.json()
        
        print("\nAvailable Models:")
        print("-" * 80)
        
        for model_name, model_info in models['available_models'].items():
            status = "✓ Loaded" if model_info['loaded'] else "✗ Not Loaded"
            print(f"\n{model_name.upper()}")
            print(f"  Status: {status}")
            print(f"  Description: {model_info['description']}")
            print(f"  Path: {model_info['path']}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


# Example 6: Get Features Information
def example_features_info():
    """Get information about all features used in predictions"""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Features Used in Predictions")
    print("=" * 80)
    
    try:
        response = requests.get(f"{API_URL}/features-info")
        response.raise_for_status()
        features = response.json()
        
        print("\nFeature Categories:")
        for category, feature_dict in features.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            for feature, description in feature_dict.items():
                print(f"  • {feature}: {description}")
                
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


# Example 7: Custom Video with Different Parameters
def example_custom_parameters():
    """Demonstrate different parameter combinations"""
    print("\n" + "=" * 80)
    print("EXAMPLE 7: Testing Different Parameter Combinations")
    print("=" * 80)
    
    base_video = {
        "title": "Amazing Discovery That Will Change Your Life",
        "description": "You won't believe what we found! Check it out.",
        "model": "random_forest"
    }
    
    test_cases = [
        {
            "name": "Medium Engagement",
            "view_count": 100000,
            "likes": 3000,
            "comment_count": 500,
            "publish_hour": 12,
        },
        {
            "name": "High Engagement",
            "view_count": 1000000,
            "likes": 80000,
            "comment_count": 20000,
            "publish_hour": 18,
        },
        {
            "name": "Low Engagement",
            "view_count": 10000,
            "likes": 100,
            "comment_count": 20,
            "publish_hour": 3,
        },
    ]
    
    print("\nImpact of Engagement Metrics on Predictions:")
    print("-" * 80)
    print(f"{'Engagement Level':<20} {'Trending':<12} {'Probability':<15}")
    print("-" * 80)
    
    for test in test_cases:
        payload = {**base_video}
        payload['view_count'] = test['view_count']
        payload['likes'] = test['likes']
        payload['comment_count'] = test['comment_count']
        payload['publish_hour'] = test['publish_hour']
        
        try:
            response = requests.post(f"{API_URL}/predict", json=payload)
            result = response.json()
            print(f"{test['name']:<20} {str(result['is_trending']):<12} "
                  f"{result['probability']:.1%}")
        except requests.exceptions.RequestException as e:
            print(f"{test['name']:<20} Error: {str(e)[:30]}")


def main():
    """Run all examples"""
    print("\n" + "=" * 80)
    print(" " * 20 + "ViralLens AI - API Examples")
    print("=" * 80)
    print(f"\nConnecting to API at: {API_URL}")
    
    try:
        # Quick health check first
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code != 200:
            print("⚠ Warning: API health check failed!")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API!")
        print(f"Please ensure the API is running at {API_URL}")
        print("\nTo start the API, run:")
        print("  python main.py")
        print("or")
        print("  uvicorn main:app --reload")
        return
    
    # Run all examples
    example_health_check()
    example_models_info()
    example_single_prediction()
    example_compare_models()
    example_batch_prediction()
    example_features_info()
    example_custom_parameters()
    
    print("\n" + "=" * 80)
    print("All examples completed!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
