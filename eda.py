
def eda():
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    from io import StringIO
   
    st.markdown(f"# Análisis Explotario de Datos")
    st.write("""
        En este análisis exploratorio de datos, nos enfocaremos en 
        comprender las variables y patrones subyacentes que 
        afectan la retención de clientes. 
    """)
    st.divider()

    if "df" not in st.session_state:
        st.write("Debe Ingresar el dataset primero, Dirijase a la pagina principal.") 
    else:
        data = st.session_state.df
        seleccion_grafica_cate = st.sidebar.selectbox('Selecciona una Variable Categórica', list(data.select_dtypes(include='object').columns))
        seleccion_grafica_nume = st.sidebar.selectbox('Selecciona una Variable Numérica', list(data.select_dtypes(exclude='object').columns))

        info = StringIO()
        data.info(buf=info)
        #Imprime La información
        st.text(str(info.getvalue()))
        
        st.metric("El número de filas es:",data.shape[0])
        
        st.write(data.isnull().sum().sort_values(ascending=False))
        st.write(data.duplicated().sum())
        st.write(data.nunique())
        st.write(data.select_dtypes(include='object').shape[1])
        st.write(data.describe().round(2))
        st.write(data.corr(numeric_only=True))
        
        
        # Primera fila
        st.markdown('### Metrics')
        col1, col2, col3, col4,col5 = st.columns(5)
        col1.metric("Número de Filas", data.shape[0])
        col2.metric("Número de Columnas", data.shape[1])
        col3.metric("Datos Duplicados", data.duplicated().sum())
        col4.metric("Variables Categóricas",data.select_dtypes(include='object').shape[1])
        col5.metric("Variables Numéricas",data.select_dtypes(exclude='object').shape[1])

        #Fila 2
        st.markdown('### Gráficos de las variables Categóricas')
        c1, c2 = st.columns((5,5))
        valores_categoricas = data[seleccion_grafica_cate].value_counts()
        valores_numericas = data[seleccion_grafica_nume]
        
        
        with c1:
            import plotly.graph_objects as go
            import streamlit as st

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=valores_categoricas.index,
                y=valores_categoricas,
                text=valores_categoricas,
                textposition='auto',
                hovertemplate='%{x}: <br>valores_categoricas: %{y}',
            ))

            fig.update_layout(
                title=f"Gráfico de Barras - {seleccion_grafica_cate}",
                xaxis_title="Género",
                yaxis_title="valores_categoricas",
                font=dict(size=12),
                width=500,
                height=500
            )

            st.plotly_chart(fig)

        
        with c2:
            
            fig = go.Figure()

            fig.add_trace(go.Pie(
                labels=valores_categoricas.index,
                values=valores_categoricas.values,
                textinfo='label+percent',
                insidetextorientation='radial',
                hovertemplate='%{label}: <br>valores_categoricas: %{value} <br>Porcentaje: %{percent}',
                showlegend=True
            ))

            fig.update_layout(
                title=f"Gráfico Circular - {seleccion_grafica_cate}",
                title_x=0.5,
                font=dict(size=15),
                width=500,
                height=500
            )

            st.plotly_chart(fig)

        # Row C
        st.markdown('### Variables Nunéricas')
        import plotly.graph_objects as go
        import streamlit as st

        fig = go.Figure()
        
        for variable in data[seleccion_grafica_cate].unique():
            fig.add_trace(go.Box(
                x=data[seleccion_grafica_cate][data[seleccion_grafica_cate] == variable],
                y=data[seleccion_grafica_nume][data[seleccion_grafica_cate] == variable],
                hovertemplate='Género: %{x}<br>Edad: %{y}',
                    
            ))

        fig.update_layout(
            title=f"Gráfico Boxplot - {seleccion_grafica_cate}",
            xaxis_title=seleccion_grafica_cate,
            yaxis_title=seleccion_grafica_nume,
            font=dict(size=12)
        )

        st.plotly_chart(fig)
        import plotly.graph_objects as go
        import streamlit as st

        fig = go.Figure()

        fig.add_trace(go.Histogram(
            x=valores_numericas,
            nbinsx=5,
            marker_color='#0d6efd',
            hovertemplate='Edad: %{x}<br>valores_categoricas: %{y}'
        ))

        fig.update_layout(
            title=f"Histograma - {seleccion_grafica_cate}",
            xaxis_title="Edad",
            yaxis_title="valores_categoricas",
            font=dict(size=12)
        )

        st.plotly_chart(fig)


        


