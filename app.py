# app.py (CONTROLADOR)
# =========================
import streamlit as st
from modelo import *
from vista import *

st.set_page_config(page_title="Cuestionario VF", page_icon="👁️", layout="centered")
aplicar_estilos()
init_state()

indice = st.session_state.indice_actual

if indice == -1:
    vista_bienvenida()

elif 0 <= indice < len(preguntas):
    vista_preguntas_generales(indice)

elif indice == len(preguntas):
    vista_filtro_conduccion()

elif len(preguntas) < indice <= len(preguntas) + len(preguntas_conduccion):
    vista_preguntas_conduccion(indice)

else:
    vista_resultados()
