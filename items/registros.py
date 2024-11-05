import streamlit as st
import pandas as pd
from datetime import datetime

FILE = "data/registros.csv"
FILE_OPCIONES = "data/TB_CENTRO_VACUNACION.csv"

def registro():
    st.title("REGISTROS")
    if st.button("CREAR REGISTRO", icon=":material/add:"):
        crear_registro()
    st.header("")
    df = listar()

    # GENERAR TABLA
    for index, row in df.iterrows():
        col_id, col_nombre, col_apellido, col_edad, col_idcentro, col_fecha, col_editar, col_delete = st.columns(8)
        
        col_id.write("**ID**") if index == 0 else None
        col_id.write(row["ID"])
        
        col_nombre.write("**Nombre**") if index == 0 else None
        col_nombre.write(row["Nombre"])
        
        col_apellido.write("**Apellido**") if index == 0 else None
        col_apellido.write(row["Apellido"])
        
        col_edad.write("**Edad**") if index == 0 else None
        col_edad.write(row["Edad"])
        
        col_idcentro.write("**SedeID**") if index == 0 else None
        col_idcentro.write(row["id_centro_vacunacion"])
        
        col_fecha.write("**Fecha**") if index == 0 else None
        col_fecha.write(row["Fecha"])

        col_editar.write("**Editar**") if index == 0 else None
        if col_editar.button("", key=f"btn_edit_{index}", icon=":material/edit:"):
            crear_registro(row)

        col_delete.write("**Eliminar**") if index == 0 else None
        if col_delete.button("", key=f"btn_delete_{index}", icon=":material/delete:"):
            eliminar_registro(row)


    return 



def listar():
    try:
        return pd.read_csv(FILE, sep=";", index_col=False)
    except FileNotFoundError:
        return pd.DataFrame(columns=["ID", "Nombre", "Apellido", "Edad", "id_centro_vacunacion", "Fecha"])



def crear(nombre, apellido, edad, id_centro, fecha):
    df = listar()
    new_id = df["ID"].max() + 1 if not df.empty else 1
    new_user = pd.DataFrame([[new_id, nombre, apellido, edad, id_centro, fecha]], columns=["ID", "Nombre", "Apellido", "Edad", "id_centro_vacunacion", "Fecha"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(FILE, sep=";", index=False)


def eliminar(user_id):
    df = listar()
    df = df[df["ID"] != user_id]
    df.to_csv(FILE, index=False, sep=";")



def update(user_id, nombre, apellido, edad, id_centro_vacunacion, fecha):
    df = listar()
    df.loc[df["ID"] == user_id, ["Nombre", "Apellido", "Edad", "id_centro_vacunacion", "Fecha"]] = nombre, apellido, edad, id_centro_vacunacion, fecha
    df.to_csv(FILE, index=False, sep=";")


@st.dialog("Registro")
def crear_registro(item = None):
    if item is not None:
        st.header("Editar")
        nombre = st.text_input("Nombre", value=item["Nombre"])
        apellido = st.text_input("Apellido", value=item["Apellido"])
        edad = st.number_input("Edad", min_value=0, max_value=120, value=item["Edad"])

        opciones = pd.read_csv(FILE_OPCIONES, sep=";", usecols=["id_centro_vacunacion", "nombre"])

        default = opciones[opciones["id_centro_vacunacion"] == item["id_centro_vacunacion"]]["nombre"].iloc[0]
        
        filtro = st.text_input("Buscar sede:", value=default)
        opciones_filtrado = opciones[opciones["nombre"].str.contains(filtro, case=False)]
        seleccion = st.selectbox("Selecciona la sede", opciones_filtrado["nombre"])
        id_centro = opciones_filtrado[opciones_filtrado["nombre"] == seleccion]["id_centro_vacunacion"].iloc[0]

        #id_centro = st.number_input("id_centro_vacunacion", min_value=0, max_value=120, value=item["id_centro_vacunacion"])
        fecha = st.date_input("Fecha", value=datetime.strptime(item["Fecha"], "%Y-%m-%d").date())
        
        if st.button("Editar"):
            update(item.ID, nombre, apellido, edad, id_centro, fecha)
            st.toast('Usuario Editado')
            st.rerun()
    else:
        st.header("Crear")
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        edad = st.number_input("Edad", min_value=0, max_value=120)

        opciones = pd.read_csv(FILE_OPCIONES, sep=";", usecols=["id_centro_vacunacion", "nombre"])
        filtro = st.text_input("Buscar sede:")
        opciones_filtrado = opciones[opciones["nombre"].str.contains(filtro, case=False)]
        seleccion = st.selectbox("Selecciona la sede", opciones_filtrado["nombre"])
        id_centro = opciones_filtrado[opciones_filtrado["nombre"] == seleccion]["id_centro_vacunacion"].iloc[0]

        fecha = st.date_input("Fecha", value="today")
        if st.button("Submit"):
            #st.session_state.vote = {"item": item, "reason": reason}
            crear(nombre, apellido, edad, id_centro, fecha)
            st.toast('Usuario Registrado')
            st.rerun()
            
    return 


@st.dialog("Registro")
def eliminar_registro(item):
    nombre = item["Nombre"]
    apellido = item["Apellido"]
    st.header(f"¿Estás seguro de eliminar el registro de {nombre} {apellido}?")

    if st.button("Eliminar"):
        eliminar(item["ID"])
        st.rerun()
    return 