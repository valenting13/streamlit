import streamlit as st
from inicio import cargar_archivo
from eda import eda
from entrenamiento import entrenamiento
from preprocesamiento import preprocesamiento
from prediccion import prediccion
from reporte import reporte

st.set_page_config(layout='wide', initial_sidebar_state='expanded')


configuracion="""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""
st.markdown(configuracion,unsafe_allow_html=True)
nombresPaginas = {
    "Inicio": cargar_archivo,
    "Análisis Exploratorio de Datos": eda,
    "Preprocesamiento de Datos":preprocesamiento,
    "Entrenamiento y Prueba": entrenamiento,
    "Predicción": prediccion,
    "Reporte": reporte
}

nombre_paginas = st.sidebar.selectbox("Escoja una página", nombresPaginas.keys())
nombresPaginas[nombre_paginas]()