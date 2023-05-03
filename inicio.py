import streamlit as st
import pandas as pd
from io import StringIO


  
def cargar_archivo():
    
    uploaded_file = st.file_uploader("Cargue su archivo CSV", type=["csv"])
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        st.session_state.df = pd.read_csv(uploaded_file)
        st.write(f"Contenido del archivo {st.session_state.uploaded_file.type}")
        # Inicializar el estado del botón si no existe
        mostrar_dataset = st.checkbox("Mostrar dataset")

        # Mostrar el dataset si la casilla de verificación está marcada
        if mostrar_dataset:
            st.write(st.session_state.df)
    elif "uploaded_file" in st.session_state:
        st.markdown(f"Archivo previamente subido: **{st.session_state.uploaded_file.name}**")
        st.write("Contenido del archivo CSV:")
        col1, col2 = st.columns(2)
        with col1:
            st.text("")
        with col2:
            col2_1, col2_2= st.columns(2)
            with col2_1:
                botonMostrar = st.button("Mostrar Dataset")
        if botonMostrar:
            st.write(st.session_state.df)
            with col2_2:
                st.button("Ocultar Dataset")



