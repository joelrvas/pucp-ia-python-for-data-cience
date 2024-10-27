import streamlit as st
import pandas as pd


## Functions utiles
def cargar_datos(filename):
    return pd.read_csv(filename, delimiter=';')

def obtener_listas_unicas(df):
    departamentos = ['Seleccione'] + list(df['departamento'].unique())
    provincias = ['Seleccione']
    distritos = ['Seleccione']
    return departamentos, provincias, distritos

def crear_combobox(df, departamentos, provincias, distritos):
    departamento_seleccionado = st.selectbox('Selecciona el Departamento', departamentos)
    if departamento_seleccionado != 'Seleccione':
        provincias = ['Seleccione'] + list(df[df['departamento'] == departamento_seleccionado]['provincia'].unique())
    provincia_seleccionada = st.selectbox('Selecciona la Provincia', provincias)
    if provincia_seleccionada != 'Seleccione':
        distritos = ['Seleccione'] + list(df[(df['departamento'] == departamento_seleccionado) & 
                                              (df['provincia'] == provincia_seleccionada)]['distrito'].unique())
    distrito_seleccionado = st.selectbox('Selecciona el Distrito', distritos)
    return departamento_seleccionado, provincia_seleccionada, distrito_seleccionado

def obtener_id_ubigeo(df, depto_sel, prov_sel, dist_sel):
    if depto_sel == 'Seleccione' or prov_sel == 'Seleccione' or dist_sel == 'Seleccione':
        return None
    resultado = df[(df['departamento'] == depto_sel) & 
                   (df['provincia'] == prov_sel) & 
                   (df['distrito'] == dist_sel)]
    if not resultado.empty:
        return resultado['id_ubigeo'].values[0]
    else:
        return None


############## Init Html #################################
# Título del proyecto
st.title('Gobierno del Perú - Covid')

# Carga de datos
df_ubigeos = cargar_datos('TB_UBIGEOS.csv')
df_vacunacion = cargar_datos('TB_CENTRO_VACUNACION.csv')
departamentos, provincias, distritos = obtener_listas_unicas(df_ubigeos)
depto_sel, prov_sel, dist_sel = crear_combobox(df_ubigeos, departamentos, provincias, distritos)
nombre_busqueda = st.text_input('Buscar por centro de vacunación')

# Unir los datos de vacunación y ubigeos
df_join_ubigeo_centros = pd.merge(df_vacunacion, df_ubigeos, how='left', left_on='id_ubigeo', right_on='id_ubigeo')
df_join_ubigeo_centros = df_join_ubigeo_centros[['departamento', 'provincia', 'distrito', 'id_ubigeo', 'id_centro_vacunacion', 'nombre', 'latitud_x', 'longitud_x', 'entidad_administra', 'id_eess']]

# Mostrar resultados según el tipo de búsqueda
if nombre_busqueda:
    resultado_busqueda = df_join_ubigeo_centros[df_join_ubigeo_centros['nombre'].str.contains(nombre_busqueda, case=False, na=False)]
    st.write(f"Resultados de la búsqueda por nombre '{nombre_busqueda}':")
    st.write(resultado_busqueda)
else:
    # Filtrar por id_ubigeo seleccionado
    if depto_sel != 'Seleccione' and prov_sel != 'Seleccione' and dist_sel != 'Seleccione':
        id_ubigeo = obtener_id_ubigeo(df_ubigeos, depto_sel, prov_sel, dist_sel)
        if id_ubigeo:          
            resultado_centro_vacunacion = df_join_ubigeo_centros.loc[df_join_ubigeo_centros['id_ubigeo'] == id_ubigeo,['departamento', 'provincia', 'distrito', 'id_ubigeo', 'nombre', 'id_centro_vacunacion', 'entidad_administra', 'latitud_x', 'longitud_x']]
            st.write("Centro de vacunación correspondiente al ID de Ubigeo seleccionado:")           
            st.write(resultado_centro_vacunacion)
        else:
            st.write('No se encontró el ID de Ubigeo correspondiente a la selección.')
    else:
        st.write('Por favor, selecciona Departamento, Provincia y Distrito.')
