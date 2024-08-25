import streamlit as st
import pickle 
import pandas as pd
import requests

API_KEY = "5e28e7dc2560e3bdc7887a4f7146c22b"
API_Read_Access_Token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1ZTI4ZTdkYzI1NjBlM2JkYzc4ODdhNGY3MTQ2YzIyYiIsIm5iZiI6MTcyNDUxODg4My4zNjUyMjMsInN1YiI6IjY2Y2ExMGMwYWI5NjgyNjAzOGRlMDc2ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.7nxsERmZctZrxzXZRrLEfr-EjoiKRO_KJy2aM20XHOM"

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, API_KEY))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

def recommend(movie):
    movieIdx = movies[movies['title'] == movie].index[0]
    distances = similarity[movieIdx]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x : x[1])[1 : 6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('sim.pickle', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Choose your favourite movie here',
    movies['title'].values
)

if st.button('Recommend'):
    recommendations, recommended_movies_posters = recommend(selected_movie_name)
    # for i in recommendations:
    #     st.write(i)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(recommended_movies_posters[0])
    with col2:
        st.text(recommendations[1])
        st.image(recommended_movies_posters[1])
    with col3:
        st.text(recommendations[2])
        st.image(recommended_movies_posters[2])
    with col4:
        st.text(recommendations[3])
        st.image(recommended_movies_posters[3])
    with col5:
        st.text(recommendations[4])
        st.image(recommended_movies_posters[4])