import streamlit as st
import pandas as pd
from powerbiclient import QuickVisualize, get_dataset_config, Report
from powerbiclient.authentication import DeviceCodeLoginAuthentication

def reporte(): 
    uploaded_file = st.file_uploader("Suba su archivo Excel aquí", type=["xlsx", "xls"])
    if uploaded_file is not None:
        dataset = pd.read_excel(uploaded_file)
        st.markdown('''
                    <iframe title="Transporte y Logistica - Instructor" width="1100" height="673.5" src="https://app.powerbi.com/view?r=eyJrIjoiZjVkODFhNjEtY2RhMy00ODAwLWExNGUtOWM0MTJkNjM1NDFkIiwidCI6ImQyZGZkYjc0LWZiNDItNGMzYi04ZGFkLTZiNzg1NzlmMmM4ZCIsImMiOjR9" frameborder="0" allowFullScreen="true"></iframe>
                    ''', unsafe_allow_html=True)


