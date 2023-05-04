import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from io import BytesIO

@st.cache_data(persist="disk")
def columnas():
    if "data" in st.session_state:
        if "boton_eliminar" in st.session_state:
            if st.session_state.boton_eliminar:
                data=st.session_state.data
                columnas = data.columns
                if st.session_state.boton_eliminar ==False:
                    data=st.session_state.data
                    columnas = data.columns
    return columnas
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Hoja1')
    writer.save()
    output.seek(0)
    return output

def prediccion():
    modelo_entrenado = st.file_uploader("Suba el Modelo Entrenado",type=["pkl"])
    
    if modelo_entrenado is not None:
        carga_modelo = pickle.load(modelo_entrenado)
        datos_nuevos = st.sidebar.file_uploader("Suba los datos que desea predecir", type=["csv"])
        if datos_nuevos is not None:
            dataset_ingresado = pd.read_csv(datos_nuevos)
            st.write(dataset_ingresado)
            columnas_comunes = dataset_ingresado.columns.intersection(columnas())
            dataset_nuevo = dataset_ingresado[columnas_comunes]
            st.write(dataset_nuevo)
            
            
            
        else:
            st.write("existe")
            column = columnas()
            boton_actualizar = st.button("Actualizar Columnas")
            if boton_actualizar:
                columnas.clear()
                column = columnas()
                if boton_actualizar == False:
                    columnas.clear()
                    column = columnas()
            datos_dicc = {}
            if "Genero" in column:
                genero = st.sidebar.selectbox('Genero',("Femenino","Masculino"))
                datos_dicc['genero']= genero
            if "PersonaMayor" in column:
                PersonaMayor = st.sidebar.selectbox('¿Es Una Persona Adulta Mayor?(Si =1,No=0)', (0,1))
                datos_dicc["PersonaMayor"]=PersonaMayor
            if "Socio" in column:
                Socio = st.sidebar.selectbox('¿Eres socio?', ("Si","No"))
                datos_dicc["Socio"]=Socio
            if "Dependientes" in column:
                Dependientes = st.sidebar.selectbox('¿Eres Dependiente?',("Si","No"))
                datos_dicc["Dependientes"]=Dependientes
            if "Permanencia" in column:
                Permanencia = st.sidebar.slider('¿Cuantos Meses tienes de Contrato?',0,72,29)
                datos_dicc["Permanencia"]=Permanencia
            if "ServicioTelefonico" in column:
                ServicioTelefonico = st.sidebar.selectbox('¿Tienes Servicio Telefónico?', ("Si","No"))
                datos_dicc["ServicioTelefonico"]=ServicioTelefonico
            if "VariasLineas" in column:
                VariasLineas = st.sidebar.selectbox('¿Eres socio?', ("Si","No","Sin Servicio Telefónico"))
                datos_dicc["VariasLineas"]=VariasLineas
            if "ServicioInternet" in column:
                ServicioInternet = st.sidebar.selectbox('¿Que servicio de Internet Tiene?', ("DLS","No","Fibra Óptica"))
                datos_dicc["ServicioInternet"]=ServicioInternet
            if "SeguridadLinea" in column:
                SeguridadLinea = st.sidebar.selectbox('¿Eres socio?', ("Si","No","Sin Servicio de Internet"))
                datos_dicc["SeguridadLinea"]=SeguridadLinea
            if "CopiaSeguridadLinea" in column:
                CopiaSeguridadLinea = st.sidebar.selectbox('¿Eres ?', ("Si","No","Sin Servicio de Internet"))
                datos_dicc["CopiaSeguridadLinea"]=CopiaSeguridadLinea
            if "ProteccionDispositivo" in column:
                ProteccionDispositivo = st.sidebar.selectbox('¿Es socio?', ("Si","No","Sin Servicio de Internet"))
                datos_dicc["ProteccionDispositivo"]=ProteccionDispositivo
            if "ServicioTecnico" in column:
                ServicioTecnico = st.sidebar.selectbox('¿Eres scio?', ("Si","No","Sin Servicio de Internet"))
                datos_dicc["ServicioTecnico"]=ServicioTecnico
            if "ServicioTV" in column:
                ServicioTV = st.sidebar.selectbox('¿Eres so?', ("Si","No","Sin Servicio de Internet"))
                datos_dicc["ServicioTV"]=ServicioTV
            if "ServicioPeliculas" in column:
                ServicioPeliculas = st.sidebar.selectbox('¿Eresocio?', ("Si","No","Sin Servicio de Internet"))
                datos_dicc["ServicioPeliculas"]=ServicioPeliculas
            if "Contrato" in column:
                Contrato = st.sidebar.selectbox('¿Eres soio?', ("Mensual","un anio","dos anios"))
                datos_dicc["Contrato"]=Contrato
            if "FacturacionElectronica" in column:
                FacturacionElectronica = st.sidebar.selectbox('¿Erio?', ("Si","No"))
                datos_dicc["FacturacionElectronica"]=FacturacionElectronica
            if "MetodoPago" in column:
                MetodoPago = st.sidebar.selectbox('¿Eres cio?', ("Cheque Electrónico","Cheque por Correo","Transferencia bancaria (automática)","Tarjeta de crédito (automática)"))
                datos_dicc["MetodoPago"]=MetodoPago
            if "RecargoMensual" in column:
                RecargoMensual = st.sidebar.number_input('¿Eres socio?',0.00,200.00,70.35)
                datos_dicc["RecargoMensual"]=RecargoMensual
            if "TotalRecargo" in column:
                TotalRecargo = st.sidebar.number_input('¿Eres socio?',0.00,10000.00,1000.00)
                datos_dicc["TotalRecargo"]=TotalRecargo

            dataset_nuevo = pd.DataFrame(datos_dicc, index=[0])
            st.write(dataset_nuevo)              
        
        for i in dataset_nuevo.select_dtypes(include='object').columns:
            dataset_nuevo[i] = LabelEncoder().fit_transform(dataset_nuevo[i])
        scaler = StandardScaler().fit(dataset_nuevo[["TotalRecargo"]])
        dataset_nuevo["TotalRecargo"] = scaler.transform(dataset_nuevo[["TotalRecargo"]])
        scaler = StandardScaler().fit(dataset_nuevo[["RecargoMensual"]])
        dataset_nuevo["RecargoMensual"] = scaler.transform(dataset_nuevo[["RecargoMensual"]])
        
        
        prediccion_modelo = carga_modelo.predict(dataset_nuevo)
        prediction_proba_modelo = carga_modelo.predict_proba(dataset_nuevo)
        
        col1, col2 = st.columns(2)

        with col1:
            if datos_nuevos is not None:
                st.subheader('Predicción')
                df_abandono = pd.DataFrame(prediccion_modelo,columns=["Abandono"])
                df_abandono = df_abandono.applymap(lambda x: "No" if x == 0 else "Si")
                st.write(df_abandono)
                    

                with col2:
                    st.subheader('Probabilidad de predicción')
                    df_abandono = pd.DataFrame(prediction_proba_modelo.argmax(axis=1), columns=["Abandono"])
                    df_abandono = df_abandono.applymap(lambda x: "No" if x == 0 else "Si")

                    # Extraer las probabilidades correspondientes a las predicciones
                    probabilidades = np.where(df_abandono["Abandono"] == "No", prediction_proba_modelo[:, 0], prediction_proba_modelo[:, 1])

                    # Crear un nuevo DataFrame con las predicciones y sus probabilidades
                    df_resultado = pd.DataFrame({"Abandono": df_abandono["Abandono"], "Probabilidad": probabilidades})
                    st.write(df_resultado)
                    df_unido = pd.concat([dataset_ingresado,df_resultado],axis=1)
                    
                st.download_button(
                label="Descargar El Archivo",
                data=to_excel(df_unido),
                file_name='Reporte.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            else:
                st.subheader('Predicción')
                df_abandono = pd.DataFrame(prediccion_modelo,columns=["Abandono"])
                df_abandono = df_abandono.applymap(lambda x: "No" if x == 0 else "Si")
                st.write(df_abandono )                   
        
    else:
        st.write("Debe entrenar el modelo para poder realizar la predicción")
