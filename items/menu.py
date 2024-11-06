import streamlit as st
from .centro_vacunacion import app
from .registros import registro

def pag1():
    st.title("DASHBOARD")
    return 

def pag2():
    app()
    return 

def pag3():
    registro()
    return 