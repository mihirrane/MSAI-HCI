# 1. Implementing Collaborative Filtering

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

def collaborative_filtering(ratings_df, movie_id, top_n=10):
    # Create a user-item matrix
    user_item_matrix = ratings_df.pivot(index='userId', columns='movieId', values='rating').fillna(0)
    
    # Convert to sparse matrix for efficiency
    user_item_sparse = csr_matrix(user_item_matrix.values)
    
    # Compute item-item similarity matrix
    item_similarity = cosine_similarity(user_item_sparse.T)
    
    # Get similar movies
    similar_movies = item_similarity[movie_id]
    
    # Sort and get top N similar movies
    similar_movies_indices = similar_movies.argsort()[::-1][1:top_n+1]
    similar_movie_ids = user_item_matrix.columns[similar_movies_indices]
    
    return similar_movie_ids.tolist()

# Usage:
# ratings_df = pd.read_csv('ratings.csv')
# similar_movies = collaborative_filtering(ratings_df, movie_id=1, top_n=10)

# 2. Enhancing Sentiment Analysis with BERT

from transformers import BertTokenizer, BertForSequenceClassification
import torch

class SentimentAnalyzer:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)
        self.model.eval()

    def analyze(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        probabilities = torch.softmax(outputs.logits, dim=1)
        sentiment_score = probabilities[0, 2].item() - probabilities[0, 0].item()  # Positive - Negative
        
        return sentiment_score

# Usage:
# analyzer = SentimentAnalyzer()
# sentiment_score = analyzer.analyze("This movie was fantastic! I loved every minute of it.")

# 3. Hybrid Recommendation System

def hybrid_recommendations(content_based_recs, collaborative_recs, sentiment_scores, alpha=0.5):
    # Combine content-based and collaborative recommendations
    all_recs = set(content_based_recs + collaborative_recs)
    
    # Calculate hybrid scores
    hybrid_scores = {}
    for movie_id in all_recs:
        content_score = 1 if movie_id in content_based_recs else 0
        collab_score = 1 if movie_id in collaborative_recs else 0
        sentiment = sentiment_scores.get(movie_id, 0)
        
        hybrid_scores[movie_id] = alpha * (content_score + collab_score) + (1 - alpha) * sentiment
    
    # Sort and return top recommendations
    sorted_recs = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
    return [movie_id for movie_id, _ in sorted_recs]

# Usage:
# collaborative_recs = collaborative_filtering(ratings_df, movie_id, top_n=10)
# sentiment_scores = {movie_id: analyzer.analyze(review) for movie_id, review in movie_reviews.items()}
# hybrid_recs = hybrid_recommendations(content_based_recs, collaborative_recs, sentiment_scores)

