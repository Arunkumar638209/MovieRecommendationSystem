import streamlit as st
import pickle
import requests

# Custom CSS for cinematic background
cinematic_css = """
<style>
body {
    background: url('https://images.unsplash.com/photo-1489599735734-79b4b8e3b9b5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80') no-repeat center center fixed;
    background-size: cover;
    color: #ffffff;
    font-family: 'Cinzel', serif;
}
.stApp {
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(10px);
    border-radius: 10px;
    padding: 20px;
    margin: 20px;
}
h1 {
    color: #ffd700 !important;
    text-shadow: 2px 2px 4px #000000;
    font-size: 3em;
    text-align: center;
    margin-bottom: 30px;
}
.stSelectbox div[data-baseweb="select"] {
    background-color: rgba(255, 215, 0, 0.1) !important;
    border: 2px solid #ffd700 !important;
    border-radius: 5px;
    color: #ffffff !important;
}
.stButton button {
    background-color: #b22222 !important;
    color: #ffffff !important;
    border: 2px solid #ffd700 !important;
    border-radius: 5px;
    font-weight: bold;
    transition: all 0.3s ease;
}
.stButton button:hover {
    background-color: #8b0000 !important;
    transform: scale(1.05);
}
.stText {
    color: #ffffff;
    text-shadow: 1px 1px 2px #000000;
}
.stImage {
    border: 2px solid #ffd700;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.5);
}
</style>
"""

st.markdown(cinematic_css, unsafe_allow_html=True)

def fetch_poster(movie_id):
     try:
         url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
         data=requests.get(url)
         data=data.json()
         poster_path = data['poster_path']
         full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
         return full_path
     except Exception as e:
         return "https://via.placeholder.com/500x750?text=No+Image"

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list=movies['title'].values

st.header("Movie Recommender System")

selectvalue=st.selectbox("Select movie from dropdown", movies_list)

def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movie=[]
    recommend_poster=[]
    for i in distance[1:6]:
        movies_id=movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster



if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
