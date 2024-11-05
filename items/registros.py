import streamlit as st
import pandas as pd

FILE = "data/registros.csv"

def registro():
    st.title("REGISTROS")

    st.header("Crear Usuario")
    if st.button("CREAR"):
        crear_registro()

    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    edad = st.number_input("Edad", min_value=0, max_value=120)
    id_centro = st.number_input("id_centro_vacunacion", min_value=0, max_value=120)
    fecha = st.date_input("Fecha", value="today")

    if st.button("Agregar Usuario"):
        crear(nombre, apellido, edad, id_centro, fecha)
        st.success("Usuario agregado exitosamente")

    st.header("Lista de Usuarios")
    df = listar()
    st.dataframe(df) 

    return 



def listar():

    try:
        return pd.read_csv(FILE, sep=";")
    except FileNotFoundError:
        return pd.DataFrame(columns=["ID", "Nombre", "Apellido", "Edad", "id_centro_vacunacion", "Fecha"])



def crear(nombre, apellido, edad, id_centro, fecha):
    df = listar()
    new_id = df["ID"].max() + 1 if not df.empty else 1
    new_user = pd.DataFrame([[new_id, nombre, apellido, edad, id_centro, fecha]], columns=["ID", "Nombre", "Apellido", "Edad", "id_centro_vacunacion", "Fecha"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(FILE, index=False, sep=";")


def eliminar():
    return 


def update():
    return

@st.dialog("Registro")
def crear_registro(item = None):
    if item:
        st.write(f"EDITAR")
    else:
        st.header("Crear")
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        edad = st.number_input("Edad", min_value=0, max_value=120)
        id_centro = st.number_input("id_centro_vacunacion", min_value=0, max_value=120)
        fecha = st.date_input("Fecha", value="today")
        if st.button("Submit"):
            st.session_state.vote = {"item": item, "reason": reason}
            st.rerun()
            
    return 