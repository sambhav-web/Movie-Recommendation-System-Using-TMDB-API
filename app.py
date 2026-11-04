import streamlit as st
import pandas as pd
import os
import requests
import joblib

with open('similarity.pkl','rb') as file:
  similarities=joblib.load(file)
df=pd.read_csv('movies.csv')
movie_names=len(list(df['title'].unique()))

def images_call(images):
  os.makedirs('images',exist_ok=True)
  current_loc=os.getcwd()
  config="https://api.themoviedb.org/3/configuration"
  response3=requests.get(config,params=PARAMS)
  info=response3.json()['images']
  base_url=info['secure_base_url']
  poster_sizes=info['poster_sizes']
  for image in images:
    for i in poster_sizes:
      image_url=base_url+i+image
      response4=requests.get(image_url)
      if response4.status_code==200:
        with open(f'{current_loc}/images{image}','wb') as file:
          file.write(response4.content)
        break
      else:
        pass

def recommend(movie):
  index=df[df['title']==movie].index[0]
  recommendations=similarities[index]
  recommendations=sorted(enumerate(recommendations),reverse=True,key=lambda x:x[1])[1:6]
  indexes=[i for i,j in recommendations]
  movies=[]
  posters=[]
  for i in indexes:
    movie=df[df.index==i]
    movies.append(movie['title'].values[0])
    posters.append(movie['poster_path'].values[0])
  images_call(posters)
  return movies,posters

st.title('Movie Recommendation System')
movie=st.sidebar.selectbox('Select a Movie :',movie_names)
if st.button('Recommend'):
  movies_list,image_id=recommend(movie)
  cols=st.columns(5)
  for i in range(5):
    with cols[i]:
      with open(f'{os.getcwd()}/images{image[i]}','rb') as f:
        image=f.read()
      st.image(image,movies_list[i],100)