import streamlit as st
import items.menu as menu



pg = st.navigation([
    st.Page(menu.pag1, title="Dashboard", icon=":material/empty_dashboard:"),
    st.Page(menu.pag2, title="Buscar Centro de Vacunación", icon=":material/search:"),
    st.Page(menu.pag3, title="Registros", icon=":material/app_registration:"),
])
pg.run()
