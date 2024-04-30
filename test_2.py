import streamlit as st 
import PIL as pil 
import datetime as dt

st.header('Web-сервис на основе python (streamlit)')

params = st.experimental_get_query_params()

st.text('********************************************')
param1 = params['param1'][0] if 'param1' in params else None
#param2 = params['param2'][0] if 'param2' in params else None
st.info('Param1:'+ str(param1))
st.text('********************************************')
st.text(dt.time())    
            
    