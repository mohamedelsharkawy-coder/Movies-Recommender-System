import streamlit as st
import pandas as pd
import json
import requests
from PIL import Image
from io import BytesIO
from recommendation import get_top_k_recommendations_df, movie_similarities, model, SAMPLE_MOVIES
import os

# Configure page
st.set_page_config(
    page_title="Cornflix - Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Netflix-like styling
st.markdown("""
<style>
    .main {
        background-color: #000000;
        color: #ffffff;
    }
    
    .stApp {
        background-color: #000000;
    }
    
    .title {
        color: #e50914;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .subtitle {
        color: #ffffff;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .page-button {
        background-color: #e50914;
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 18px;
        border-radius: 5px;
        cursor: pointer;
        margin: 10px;
        width: 200px;
    }
    
    .back-button {
        background-color: #333333;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
        margin-bottom: 20px;
    }
    
    .movie-card {
        background-color: #1a1a1a;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        border: 1px solid #333333;
    }
    
    .user-card {
        background-color: #1a1a1a;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        border: 1px solid #333333;
    }
    
    .rating-badge {
        background-color: #e50914;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
    }
    
    div.stButton > button {
        background-color: #e50914;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    div.stButton > button:hover {
        background-color: #b8070f;
    }
    
    .stSelectbox > div > div {
        background-color: #1a1a1a;
        color: white;
    }
    
    .stTextInput > div > div > input {
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #333333;
    }
    
    .stNumberInput > div > div > input {
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #333333;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    # Load users
    users_df = pd.read_csv(os.path.join("Deployment", 'sample_users.csv'))
    users = users_df.to_dict(orient='records')
    
    # Load movies
    movies_df = pd.read_csv(os.path.join("Deployment", 'movies.csv'))
    movies = movies_df.to_dict(orient='records')
    
    # Load user history
    with open(os.path.join("Deployment", 'user_history.json'), 'r', encoding='utf-8') as f:
        user_history = json.load(f)
    user_history = {int(k): v for k, v in user_history.items()}
    
    return users, movies, user_history

# Function to get movie poster from TMDB API
def get_movie_poster(movie_title):
    try:
        # Clean movie title (remove year)
        clean_title = movie_title.split('(')[0].strip()
        
        # TMDB API (you can get a free API key from themoviedb.org)
        api_key = "b176f8efd3f0783d9f1d9bc7c4d35f87"  # Replace with your actual API key
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={clean_title}"
        
        response = requests.get(search_url)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                poster_path = data['results'][0]['poster_path']
                if poster_path:
                    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                    return poster_url
    except:
        pass
    
    # Return placeholder image if API fails
    return "https://via.placeholder.com/300x450/1a1a1a/ffffff?text=No+Image"

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Load data
users, movies, user_history = load_data()

# Navigation
def show_back_button():
    if st.button("← Back to Home", key="back_btn"):
        st.session_state.current_page = 'home'
        st.rerun()

# Home Page
def show_home_page():
    st.markdown('<h1 class="title">🎬 CORNFLIX</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your Personal Movie Recommendation System</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown("### Choose Your Journey")
        
        if st.button("👥 Explore Users", use_container_width=True):
            st.session_state.current_page = 'users'
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🎭 Browse Movies", use_container_width=True):
            st.session_state.current_page = 'movies'
            st.rerun()

# Users Page
def show_users_page():
    show_back_button()
    
    st.markdown('<h1 class="title">👥 Users</h1>', unsafe_allow_html=True)
    
    # User search
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_id = st.number_input("Enter User ID:", min_value=1, max_value=610, value=1, step=1)
    
    with col2:
        k_recommendations = st.number_input("Number of Recommendations:", min_value=1, max_value=10, value=5, step=1)
    
    if st.button("Get User Profile & Recommendations", use_container_width=True):
        if user_id in user_history:
            # Display user history
            st.markdown(f"### User {user_id} - Viewing History")
            
            history = user_history[user_id]
            
            # Show history in a nice format
            if history:
                history_cols = st.columns(min(3, len(history)))
                for i, movie_data in enumerate(history[:6]):  # Show first 6 movies
                    with history_cols[i % 3]:
                        poster_url = get_movie_poster(movie_data['movie'])
                        try:
                            response = requests.get(poster_url)
                            img = Image.open(BytesIO(response.content))
                            st.image(img, width=150)
                        except:
                            st.image("https://via.placeholder.com/150x225/1a1a1a/ffffff?text=No+Image", width=150)
                        
                        st.markdown(f"**{movie_data['movie']}**")
                        st.markdown(f"<span class='rating-badge'>⭐ {movie_data['rating']}</span>", unsafe_allow_html=True)
                
                if len(history) > 6:
                    st.markdown(f"*... and {len(history) - 6} more movies*")
            else:
                st.warning("No viewing history found for this user.")
            
            # Get recommendations
            st.markdown("### 🎯 Personalized Recommendations")
            try:
                recommendations = get_top_k_recommendations_df(model, user_id, k_recommendations)
                
                if recommendations:
                    rec_cols = st.columns(min(3, len(recommendations)))
                    for i, movie_title in enumerate(recommendations):
                        with rec_cols[i % 3]:
                            poster_url = get_movie_poster(movie_title)
                            try:
                                response = requests.get(poster_url)
                                img = Image.open(BytesIO(response.content))
                                st.image(img, width=150)
                            except:
                                st.image("https://via.placeholder.com/150x225/1a1a1a/ffffff?text=No+Image", width=150)
                            
                            st.markdown(f"**{movie_title}**")
                            st.markdown(f"*Rank #{i+1}*")
                else:
                    st.error("Could not generate recommendations for this user.")
            except Exception as e:
                st.error(f"Error generating recommendations: {str(e)}")
        else:
            st.error(f"User {user_id} not found in the database.")

# Movies Page
def show_movies_page():
    show_back_button()
    
    st.markdown('<h1 class="title">🎭 Movies</h1>', unsafe_allow_html=True)
    
    # Movie search
    col1, col2 = st.columns([2, 1])
    
    with col1:
        movie_titles = [movie['title'] for movie in movies]
        selected_movie = st.selectbox("Select a Movie:", movie_titles)
    
    with col2:
        k_similar = st.number_input("Number of Similar Movies:", min_value=1, max_value=10, value=5, step=1)
    
    if st.button("Get Movie Profile & Similar Movies", use_container_width=True):
        # Find movie details
        movie_details = next((movie for movie in movies if movie['title'] == selected_movie), None)
        
        if movie_details:
            # Display movie profile
            st.markdown(f"### {selected_movie}")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                poster_url = get_movie_poster(selected_movie)
                try:
                    response = requests.get(poster_url)
                    img = Image.open(BytesIO(response.content))
                    st.image(img, width=300)
                except:
                    st.image("https://via.placeholder.com/300x450/1a1a1a/ffffff?text=No+Image", width=300)
            
            with col2:
                st.markdown(f"**Movie ID:** {movie_details['movieId']}")
                st.markdown(f"**Title:** {movie_details['title']}")
                st.markdown(f"**Genres:** {movie_details['genres']}")
            
            # Get similar movies
            st.markdown("### 🎯 Similar Movies")
            try:
                similar_movies = movie_similarities(selected_movie, k_similar)
                
                if not similar_movies.empty:
                    similar_titles = similar_movies.index.tolist()
                    
                    sim_cols = st.columns(min(3, len(similar_titles)))
                    for i, movie_title in enumerate(similar_titles):
                        with sim_cols[i % 3]:
                            poster_url = get_movie_poster(movie_title)
                            try:
                                response = requests.get(poster_url)
                                img = Image.open(BytesIO(response.content))
                                st.image(img, width=150)
                            except:
                                st.image("https://via.placeholder.com/150x225/1a1a1a/ffffff?text=No+Image", width=150)
                            
                            st.markdown(f"**{movie_title}**")
                            similarity_score = similar_movies[movie_title]
                            st.markdown(f"<span class='rating-badge'>Similarity: {similarity_score:.2f}</span>", unsafe_allow_html=True)
                else:
                    st.error("No similar movies found.")
            except Exception as e:
                st.error(f"Error finding similar movies: {str(e)}")
        else:
            st.error("Movie not found in the database.")

# Main app logic
def main():
    if st.session_state.current_page == 'home':
        show_home_page()
    elif st.session_state.current_page == 'users':
        show_users_page()
    elif st.session_state.current_page == 'movies':
        show_movies_page()

if __name__ == "__main__":
    main()