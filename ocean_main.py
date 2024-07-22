import streamlit as s
import streamlit_map2 as sm2, streamlit_map as sm



s.set_page_config(page_title='Sea Water Dataset',layout='wide')
with s.sidebar:
    
    rad=s.radio("Ocean Data Set Page",['Ocean DataSet','Ocean Chemical Constants']) 

if(rad=='Ocean DataSet'):
    sm.main()

elif(rad=='Ocean Chemical Constants'):
    sm2.main()
