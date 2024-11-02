import streamlit as st

# Definir las funciones para cada página
def main_page():
    st.title("COVID 2019")
    st.write("Bienvenido a la página principal sobre COVID 2019.")

def buscar_centro_vacunacion_page():
    import pages.centro_vacunacion as cv
    cv.app()

def dashboard():
    import pages.dashboard as cv
    cv.app()

# Crear un sidebar para la navegación
st.sidebar.title("Navegación")
selection = st.sidebar.radio("Ir a:", ["COVID 2019", "Centro de Vacunación"])

# Mostrar la página seleccionada
if selection == "COVID 2019":
    dashboard()
elif selection == "Centro de Vacunación":
    buscar_centro_vacunacion_page()

# CSS personalizado para ocultar los elementos de navegación
hide_streamlit_style = """
         <style>
            [data-testid="stSidebar"][aria-expanded="true"] {
                min-width: 0px;
                max-width: 0px;
                overflow: hidden;
            }
            [data-testid="stSidebar"][aria-expanded="true"] {
                min-width: 250px;
                max-width: 250px;
                overflow: hidden;
            }
            [data-testid="stSidebarNavItems"] {
                display: none;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
