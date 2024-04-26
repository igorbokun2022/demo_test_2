import streamlit as st 
import PIL as pil 
import datetime as dt

st.header('Web-сервис на основе python (streamlit)')
st.info(st.server.request)

if st.server.request == 'bar':
    st.text('********************************************')
    #df=dt.time()     
    #st.server.({'data': df})
  # And .respond() would cause the script to finish executing immediately.