# view.py (VISTA)
# =========================
import streamlit as st
from modelo import *



def aplicar_estilos():

    # --- CSS PERSONALIZADO (DISEÑO BLINDADO Y SIN HUECOS) ---
    st.markdown("""
        <style>
        /* 1. Ocultar cabecera, menú y pie de página */
        header { visibility: hidden !important; }
        #MainMenu { visibility: hidden !important; }
        footer { visibility: hidden !important; }
        
        /* 2. Quitar el hueco en blanco gigante de la parte superior */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 0rem !important;
        }
        
        /* 3. Botones principales cómodos */
        div.stButton > button:first-child {
            padding: 12px 20px !important; 
            font-weight: bold !important;  
            border-radius: 8px !important; 
        }
        
        /* 4. Opciones de respuesta separadas para pulsar fácil */
        div.stRadio > div[role="radiogroup"] label {
            padding-top: 10px !important;   
            padding-bottom: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)


# SISTEMA DE NAVEGACIÓN (Paginación)
def init_state():
    if "indice_actual" not in st.session_state:
        st.session_state.indice_actual = -1
    if "respuestas" not in st.session_state:
        st.session_state.respuestas = {}
    if "conduce" not in st.session_state:
        st.session_state.conduce = None


def avanzar():
    st.session_state.indice_actual += 1

def retroceder():
    st.session_state.indice_actual -= 1

def reiniciar():
    st.session_state.clear()
    st.session_state.indice_actual = -1

def mostrar_pregunta(pregunta, key):
    st.markdown(f"### {pregunta}")

    if pregunta in imagenes_preguntas:
        try:
            st.image(imagenes_preguntas[pregunta], width=350)
        except Exception:
            st.error("No se pudo cargar la imagen asociada.")

    opciones_lista = list(opciones.keys())

    respuesta_previa = opciones_lista[0]
    if pregunta in st.session_state.respuestas:
        for k, v in opciones.items():
            if v == st.session_state.respuestas[pregunta]:
                respuesta_previa = k
                break

    seleccion = st.radio("", opciones_lista,
                         index=opciones_lista.index(respuesta_previa),
                         key=key,
                         label_visibility="collapsed")

    st.session_state.respuestas[pregunta] = opciones[seleccion]

# ---------- VISTAS ----------

def vista_bienvenida():
    st.title("👁️ Cuestionario de Visión Funcional")
    st.write("---")
    st.markdown("""Este cuestionario ayuda a evaluar su visión funcional.""")
    st.button("Comenzar ➡️", on_click=avanzar, use_container_width=True)


def vista_preguntas_generales(indice):
    progreso = (indice + 1) / (len(preguntas) + 1)
    st.progress(progreso)

    mostrar_pregunta(preguntas[indice], f"radio_{indice}")

    col1, col2 = st.columns(2)
    with col1: st.button("Siguiente ➡️", on_click=avanzar, use_container_width=True)
    with col2: st.button("⬅️ Anterior", on_click=retroceder, use_container_width=True)


def vista_filtro_conduccion():
    st.markdown("### 🚗 Conducción")

    indice_previo = 1 if st.session_state.conduce == "No" else 0
    conduce = st.radio("¿Actualmente conduce o prevé la necesidad de conducir?",
                       ["Sí", "No"], index=indice_previo)

    st.session_state.conduce = conduce

    def siguiente():
        if conduce == "No":
            st.session_state.indice_actual = len(preguntas) + len(preguntas_conduccion) + 1
        else:
            avanzar()

    col1, col2 = st.columns(2)
    with col1: st.button("Siguiente ➡️", on_click=siguiente, use_container_width=True)
    with col2: st.button("⬅️ Anterior", on_click=retroceder, use_container_width=True)

def vista_preguntas_conduccion(indice):
    idx = indice - len(preguntas) - 1

    st.markdown("### 🚗 Conducción")
    mostrar_pregunta(preguntas_conduccion[idx], f"radio_cond_{idx}")

    col1, col2 = st.columns(2)

    if idx == len(preguntas_conduccion) - 1:
        with col1: st.button("✅ Calcular resultados", on_click=avanzar, use_container_width=True)
    else:
        with col1: st.button("Siguiente ➡️", on_click=avanzar, use_container_width=True)

    with col2: st.button("⬅️ Anterior", on_click=retroceder, use_container_width=True)

def vista_resultados():
    st.title("📋 Resultados del Cuestionario")

    puntos_obtenidos, puntos_maximos = calcular_resultados()

    if puntos_maximos > 0:
        porcentaje = round((puntos_obtenidos * 100) / puntos_maximos, 1)

        st.success("¡Gracias! Muestre esta pantalla a su oftalmólogo.")
        st.metric("Puntuación VF", f"{porcentaje} / 100")

        if st.session_state.conduce == "Sí":
            st.info("🚗 Paciente conductor activo.")
        else:
            st.info("ℹ️ El paciente no conduce.")
    else:
        st.warning("Sin respuestas válidas.")

    st.button("🔄 Nuevo paciente", on_click=reiniciar, use_container_width=True)
