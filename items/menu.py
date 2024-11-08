import streamlit as st
from .centro_vacunacion import app
from .registros import registro
from .graficoBarras import appGraficos

def pag1():
    st.title("DASHBOARD")
    appGraficos()      
    return 

def pag2():
    app()
    return 

def pag3():
    registro()
    return 

def pag4():
    st.title("MAPA ANIMADO")
    with open("static/grafico.html", "r", encoding='utf-8') as file:
        html_content = file.read()

    st.components.v1.html(html_content, height=1000)
    return 