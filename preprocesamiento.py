def preprocesamiento():
    import streamlit as st
    

   
    
    

    st.markdown("# Preprocesamiento de Datos")
    st.markdown("<h1 style='text-align: center; color: red;'>Some title</h1>", unsafe_allow_html=True)


    if "df" not in st.session_state:
        st.warning("Debe ingresar el dataset primero, diríjase a la página principal.")
    else:
        if st.session_state.get("original_df") is None:
            st.session_state.original_df = st.session_state.df.copy()

        reset_button = st.button("Restablecer Preprocesado")
        if reset_button:
            st.session_state.df = st.session_state.original_df.copy()
            st.session_state.predf = st.session_state.df.copy()
            st.write("El dataset ha sido restablecido.")

        if "predf" not in st.session_state:
            st.session_state.predf = st.session_state.df.copy()
        st.session_state.data = st.session_state.predf
        
        col_nulo,col2 = st.columns(2)
        with col_nulo: 
            st.markdown("### Eliminar Columnas")               
            st.session_state.seleccion_nulo = st.multiselect("Escoja las variables a eliminar:", st.session_state.data.columns)
            st.session_state.boton_eliminar = st.button("Eliminar")
            if st.session_state.boton_eliminar:
                st.session_state.data = st.session_state.data.drop(st.session_state.seleccion_nulo, axis=1)
                st.session_state.predf = st.session_state.predf.drop(st.session_state.seleccion_nulo, axis=1)
                st.write(st.session_state.data)
                
        with col2:
            st.markdown("### Transformar Valores Vacios Categóricos")
            col_selec, col_boton = st.columns(2)
            with col_selec:
                seleccion_cate = st.multiselect("Escoja la(s) variable(s):", st.session_state.data.select_dtypes(include='object').columns)
                seleccion_metodo_cate = st.selectbox("Elija la técnica para transformar",["SimpleImputer"])
                seleccion_tecnica_cate = st.selectbox("Elija el método",("most_frequent","constant"))
                if seleccion_tecnica_cate == "constant":
                    fill_value = st.text_input("Con qué valor desea reemplazar")
                else:
                    fill_value = None
            with col_boton:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                boton_quitarcate = st.button("Reemplazar")
                if boton_quitarcate:
                    if seleccion_metodo_cate == "SimpleImputer":
                        categorico = SimpleImputer(strategy=seleccion_tecnica_cate,fill_value=fill_value)
                        categorico.fit_transform(st.session_state.data[seleccion_cate])
                        st.write("Valores nulos reemplazados")                 
            
        st.divider()
        col_label,col_standar=st.columns(2)
        with col_label:
            st.markdown("### Transformar Valores Vacios Numéricos")
            col_selec, col_boton = st.columns(2)
            with col_selec:
                seleccion_nume = st.multiselect("Escoja la(s) variable(s):", st.session_state.data.select_dtypes(include=['int',"float"]).columns)
                seleccion_metodo_nume = st.selectbox("Elija la técnica para transformar",("SimpleImputer","KNNImputer","IterativeImputer"))
                if seleccion_metodo_nume =="SimpleImputer":
                    seleccion_tecnica_nume = st.selectbox("Elija el método",("mean","median"))
                elif seleccion_metodo_nume == "KNNImputer":
                    seleccion_knn = st.slider("Escoja el número de muestras",0,100,5,key="seleccion_knn")
                    
                
            with col_boton:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                boton_quitarnume = st.button("Reemplazar Nulos")
                if boton_quitarnume:
                    if seleccion_metodo_nume =="SimpleImputer": 
                        from sklearn.impute import SimpleImputer
                        categorico = SimpleImputer(strategy=seleccion_tecnica_nume)
                        categorico.fit_transform(st.session_state.data[seleccion_nume])
                        st.write("Valores nulos reemplazados")
                    elif seleccion_metodo_nume == "KNNImputer":
                        from sklearn.impute import KNNImputer
                        categorico = KNNImputer(n_neighbors=seleccion_knn)
                        categorico.fit_transform(st.session_state.data[seleccion_nume])
                        st.write("Valores nulos reemplazados")    
                            
        with col_standar:
            st.write("")
            # Nuevo código
        st.divider()
        st.session_state.boton_pasos_no_realizados = st.button("Pulse aquí cuando haya terminado")
        if st.session_state.boton_pasos_no_realizados:
            for i in st.session_state.data.select_dtypes(include='object').columns:
                from sklearn.preprocessing import LabelEncoder
                st.session_state.data[i] = LabelEncoder().fit_transform(st.session_state.data[i])
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler().fit(st.session_state.data[["TotalRecargo"]])
            st.session_state.data["TotalRecargo"] = scaler.transform(st.session_state.data[["TotalRecargo"]])
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler().fit(st.session_state.data[["RecargoMensual"]])
            st.session_state.data["RecargoMensual"] = scaler.transform(st.session_state.data[["RecargoMensual"]])
 
            
        
        
        
                
                

                
