from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle
import os

############################ Preparations ###################################

# Read ratings and movies dataframes
ratings = pd.read_csv(os.path.join("Deployment", "ratings.csv"))
movies = pd.read_csv('movies.csv')

# Merge both dataframes in 1 dataframe
data = pd.merge(ratings, movies, on="movieId")

# Make user_idx and movie_idx
user_encoder = LabelEncoder()
data['user_idx'] = user_encoder.fit_transform(data['userId'])

movie_encoder = LabelEncoder()
data['movie_idx'] = movie_encoder.fit_transform(data['movieId'])

# Make utility matrix
user_item_matrix = data.pivot_table(index='user_idx', columns='title', values='rating')
user_item_filled = user_item_matrix.fillna(0)

# Make cosine similarity
item_similarity = cosine_similarity(user_item_filled.T)
item_similarity_df = pd.DataFrame(item_similarity, index=user_item_filled.columns, columns=user_item_filled.columns)

# Load the model
try:
    with open('Best_model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print("Warning: Best_model.pkl not found. Please make sure the model file is in the correct directory.")
    model = None

# Sample Movies for export
SAMPLE_MOVIES = movies.to_dict(orient='records')

#################################### User Recommendation #########################################

def get_top_k_recommendations_df(model, user_id, k=10):
    """
    Get top k movie recommendations for a specific user
    
    Args:
        model: Trained recommendation model
        user_id: User ID to get recommendations for
        k: Number of recommendations to return
    
    Returns:
        List of recommended movie titles
    """
    try:
        # Get movies already rated by the user
        rated_movies = data[data['user_idx'] == user_id]['movie_idx'].tolist()
        
        # Get all unique movies
        all_movies = data['movie_idx'].unique()
        unseen_movies = [movie for movie in all_movies if movie not in rated_movies]
        
        # Generate predictions for unseen movies
        predictions = []
        for movie in unseen_movies:
            try:
                prediction = model.predict(user_id, movie)
                predictions.append((movie, prediction.est))
            except:
                continue
        
        # Sort predictions by estimated rating (descending)
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        # Get top k predictions
        top_k = predictions[:k]
        
        # Convert movie indices back to titles
        movie_lookup = data[['movie_idx', 'title']].drop_duplicates().set_index('movie_idx').to_dict()['title']
        titles = []
        for movie_id, score in top_k:
            if movie_id in movie_lookup:
                titles.append(movie_lookup[movie_id])
        
        return titles
    
    except Exception as e:
        print(f"Error in get_top_k_recommendations_df: {str(e)}")
        return []

#######################################  Item Recommendation -> Cosine Similarity ########################################################

def movie_similarities(movie_title, top_n=10):
    """
    Find movies similar to a given movie using cosine similarity
    
    Args:
        movie_title: Title of the movie to find similarities for
        top_n: Number of similar movies to return
    
    Returns:
        Pandas Series with similar movies and their similarity scores
    """
    try:
        if movie_title not in item_similarity_df.columns:
            print(f"'{movie_title}' not found in dataset.")
            return pd.Series()
        
        # Get similarity scores for the given movie
        similarities = item_similarity_df[movie_title].sort_values(ascending=False)
        
        # Return top n similar movies (excluding the movie itself)
        return similarities.iloc[1:top_n+1]
    
    except Exception as e:
        print(f"Error in movie_similarities: {str(e)}")
        return pd.Series()

# Test functions (uncomment to test)
# if model:
#     print("Testing user recommendations:")
#     print(get_top_k_recommendations_df(model, 1, 5))

# print("\nTesting movie similarities:")
# print(movie_similarities("Toy Story (1995)", 5).index.tolist())