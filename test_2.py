import streamlit as st 
import PIL as pil 

st.header('Web-сервис: тематичеcкий онлайн анализ контента новостных каналов')
try:
    img=pil.Image.open('photo.jpg')
except:
    img=pil.Image.open('F:/_Data Sience/Веб_приложения/Streamlit/demo_test_1/photo.jpg')    
st.sidebar.image(img, width=250)