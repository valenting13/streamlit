import streamlit as st
    
def input_entrenamiento(val1, val2):
    if val1 + val2 < 100:
        diff = 100 - (val1 + val2)
        val2 += diff
    return val1, val2
    
def entrenamiento():
    st.markdown("# Preprocesamiento de Datos")
    import pandas as pd
    
    if "data" not in st.session_state:
        st.write("Debe ingresar el dataset primero, diríjase a la página principal.")
    else:
        if "data_entre" not in st.session_state:
            st.session_state.data_entre = st.session_state.predf.copy()
        data = st.session_state.data_entre
        st.sidebar.divider()
        modelo = st.sidebar.selectbox("Escoja el modelo:",("Clasificador de Regresión Logística",
                                                               "Clasificador K-vecinos más Cercanos",
                                                               "Clasificador Máquinas de Soporte Vectorial",
                                                               "Clasificador de Árboles de Decisión",
                                                               "Clasificador de Bosque Aleatorio"
                                                            ))
        randomstate= st.sidebar.number_input("Ingrese un numero", min_value=0, max_value=10000, value=0)
        train_perc = st.sidebar.slider("Porcentaje de entrenamiento:", min_value=0, max_value=100, value=80)
        
                
        
        test_perc = 0
        train_perc, test_perc = input_entrenamiento(train_perc, test_perc)
        st.sidebar.divider()
        match modelo:
            case "Clasificador de Regresión Logística":
                penalty = st.sidebar.selectbox("Penalty",("l2","l1","elasticnet"))
                C = st.sidebar.number_input("C",min_value=0.01,max_value=100.00,value=1.0)
                fit_intercept = st.sidebar.selectbox("Fit intercept",("True","False"))
                if fit_intercept == "True":
                    fit_intercept = True
                else:
                    fit_intercept = False
                solver = st.sidebar.selectbox("Solver",( 'lbfgs','newton-cg', 'liblinear', 'sag', 'saga'))
                
                parametros={
                    "penalty":penalty,
                    "C":C,
                    "fit_intercept": fit_intercept,
                    "solver": solver
                }
                from sklearn.linear_model import LogisticRegression
                modelo_entrenar = LogisticRegression(penalty=penalty,C=C,fit_intercept=fit_intercept,solver=solver)
            case "Clasificador K-vecinos más Cercanos":
                n_neighbors = st.sidebar.number_input("N neighbors",min_value=0,max_value=50,value=5)
                weights = st.sidebar.selectbox("Weights",("uniform", "distance"))
                algorithm = st.sidebar.selectbox("Algorithm",("auto","ball_tree","kd_tree","brute"))
                p = st.sidebar.selectbox("p",( 2, 1))
                
                parametros={
                    "n_neighbors":n_neighbors,
                    "weights":weights,
                    "algorithm": algorithm,
                    "p": p
                }
                from sklearn.neighbors import KNeighborsClassifier
                modelo_entrenar = KNeighborsClassifier(n_neighbors=n_neighbors,weights=weights,algorithm=algorithm,p=p)
            case "Clasificador Máquinas de Soporte Vectorial":
                penalty = st.sidebar.selectbox("Penalty",("l2","l1"))
                if penalty == "l1":
                    loss = st.sidebar.selectbox("loss",(['squared_hinge']))
                else:
                    loss = st.sidebar.selectbox("loss",( 'squared_hinge','hinge'))
                C = st.sidebar.number_input("C",min_value=0.01,max_value=100.00,value=1.0)
                fit_intercept = st.sidebar.selectbox("Fit intercept",("True","False"))
                if fit_intercept == "True":
                    fit_intercept = True
                else:
                    fit_intercept = False
                
                
                parametros={
                    "penalty":penalty,
                    "loss": loss,
                    "C":C,
                    "fit_intercept": fit_intercept
                }
                from sklearn.svm import LinearSVC
                modelo_entrenar = LinearSVC(penalty=penalty,loss=loss,C=C,fit_intercept=fit_intercept)
            case "Clasificador de Árboles de Decisión":
                criterion = st.sidebar.selectbox("criterion",("gini","entropy","log_loss"))
                splitter = st.sidebar.selectbox("splitter",("best","random"))
                max_depth = st.sidebar.selectbox("max_depth",(None,"Numeros"))
                if max_depth == "Numeros":
                    max_depth = st.sidebar.slider("max_depth",1,100,1)
                min_samples_split = st.sidebar.slider("min_samples_split",0,50,2)
                
                parametros={
                    "criterion":criterion,
                    "splitter": splitter,
                    "max_depth":max_depth,
                    "min_samples_split": min_samples_split
                }
                from sklearn.tree import DecisionTreeClassifier
                modelo_entrenar = DecisionTreeClassifier(criterion=criterion,splitter=splitter,max_depth=max_depth,min_samples_split=min_samples_split)
            case "Clasificador de Bosque Aleatorio":
                n_estimators = st.sidebar.slider("n_estimators",0,200,100)
                criterion = st.sidebar.selectbox("criterion",("gini","entropy","log_loss"))
                max_depth = st.sidebar.selectbox("max_depth",(None,"Numeros"))
                if max_depth == "Numeros":
                    max_depth = st.sidebar.slider("max_depth",1,100,1)
                min_samples_split = st.sidebar.slider("min_samples_split",0,50,2)
                
                parametros={
                    "n_estimators":n_estimators,
                    "criterion": criterion,
                    "max_depth":max_depth,
                    "min_samples_split": min_samples_split
                }
                from sklearn.ensemble import RandomForestClassifier
                modelo_entrenar = RandomForestClassifier(n_estimators=n_estimators,criterion=criterion,max_depth=max_depth,min_samples_split=min_samples_split)
            
        
        
        datos = {'Variable Dependiente':"Abandono",
                'Modelo': modelo,
                'Entrenamiento': f"{train_perc}%",
                'Prueba': f"{test_perc}%",
                "Random_State":randomstate
                    }
        entre = pd.DataFrame(datos,index=[0])
        st.write(entre)
        st.markdown(f"### Parámetros del modelo {modelo}")
        para = pd.DataFrame(parametros,index=[0])
        st.write(para)
        st.session_state.boton_entrenar = st.button("Entrenar el modelo")
        if st.session_state.boton_entrenar:
            entrenar_modelo(data,test_perc,randomstate,modelo_entrenar)
        st.session_state.boton_guardar = st.button("Guardar Modelo")
        if st.session_state.boton_guardar:
            st.success("Modelo Guardado Correctamente")
            import pickle
                # Guardamos el modelo entrenado en un archivo
            pickle.dump(entrenar_modelo(data,test_perc,randomstate,modelo_entrenar), open('modelo_entrenado.pkl', 'wb'))
        if"df" in st.session_state:
            st.markdown(f"Archivo previamente subido: **{st.session_state.uploaded_file.name}**")
            st.write(st.session_state.df)
        
            
            
def entrenar_modelo(data,test_perc,randomstate,modelo):
    import pandas as pd
    import plotly.figure_factory as ff
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import confusion_matrix
    
    x=data.drop("Abandono", axis=1)
    y=data["Abandono"]
    x_train, x_test, y_train, y_test= train_test_split(x,y,test_size=test_perc/100,random_state=randomstate)  
    model = modelo
    model.fit(x_train,y_train)
    precision = model.score(x_test, y_test)
    precision_entrena = model.score(x_train, y_train)
    st.metric("Precisión del Modelo","{0:0.2f}%".format(precision*100))
    st.metric("Precisión del modelo Entrenado","{0:0.2f}%".format(precision_entrena*100))
    y_pred_test = model.predict(x_test)
    from sklearn.metrics import accuracy_score
    st.metric("Precisión del Entrenamiento","{0:0.2f}".format(accuracy_score(y_test, y_pred_test)))
    st.write()
    cm =  confusion_matrix(y_test, y_pred_test)
    cm_matriz = pd.DataFrame(data=cm, columns=['Actual Positivo:1', 'Actual Negativo:0'],
                         index=['Prediccion Positiva:1', 'Prediccion Negativa:0'])

    fig = ff.create_annotated_heatmap(z=cm_matriz.values, x=list(cm_matriz.columns),
                                   y=list(cm_matriz.index),
                                    colorscale='YlGnBu', showscale=True, reversescale=True)

    fig.update_layout(title='Matriz de Confusión')

    st.plotly_chart(fig)
    
    y_pred1 = model.predict_proba(x_test)[:,1]
    from sklearn.metrics import roc_curve, roc_auc_score
    import plotly.graph_objs as go

    fpr, tpr , umbral = roc_curve(y_test, y_pred1, pos_label = True)
    roc_auc = roc_auc_score(y_test, y_pred1)
    # Crear un gráfico de línea utilizando Plotly
    trace0 = go.Scatter(x=fpr, y=tpr, mode='lines', name='Curva ROC (AUC = %0.2f)' % roc_auc)
    trace1 = go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Clasificador Aleatorio', line={'dash': 'dash'})
    layout = go.Layout(title='Curva ROC', xaxis={'title': 'Tasa de Falsos Positivos'}, yaxis={'title': 'Tasa de Verdaderos Positivos'}, showlegend=True)
    fig = go.Figure(data=[trace0, trace1], layout=layout)

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)
    
    return model
            

            
        
