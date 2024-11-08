import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def appGraficos():
        # Carga de datos
    df_ubigeos = cargar_datos('data/TB_UBIGEOS.csv')
    df_vacunacion = cargar_datos('data/TB_CENTRO_VACUNACION.csv')

      # Unir los datos de vacunación y ubigeos
    df_join_ubigeo_centros = pd.merge(df_vacunacion, df_ubigeos, how='left', left_on='id_ubigeo', right_on='id_ubigeo')
    df_join_ubigeo_centros = df_join_ubigeo_centros[['departamento', 'provincia', 'distrito', 'id_ubigeo', 'id_centro_vacunacion', 'nombre', 'latitud_x', 'longitud_x', 'entidad_administra', 'id_eess']]
    
    graficos(df_join_ubigeo_centros,df_ubigeos)
    
    
def cargar_datos(filename):
    return pd.read_csv(filename, delimiter=';')
    
def graficos(df_join_ubigeo_centros,df_ubigeos):
    #GRAFICO DE BARRAS

    column=st.selectbox("Organizado por: ", df_join_ubigeo_centros.columns)
    
    #Contar datos
    data_counts = df_ubigeos[column].value_counts()

    #Crea grafico de barras
    fig, ax = plt.subplots(figsize=(10,6))
    ax.bar(data_counts.index, data_counts.values, color="blue", edgecolor="blue")
    ax.set_title(f"Número de centros de vacunación por departamento {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Frecuencia")

    ax.set_xticklabels(data_counts.index, rotation=45, ha="right")
    #Mostrar el grafico
    st.pyplot(fig)
        
    return
             




    


