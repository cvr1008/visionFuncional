# vista.py
import streamlit as st
from modelo import *

def aplicar_estilos():
    st.markdown("""
        <style>
        /* 1. FULMINAR CABECERA, MENÚ, GITHUB, BARQUITO Y FOOTER */
        [data-testid="stHeader"] { display: none !important; }
        [data-testid="stToolbar"] { display: none !important; }
        [data-testid="stAppDeployButton"] { display: none !important; }
        #viewerBadgeToRender { display: none !important; }
        header { display: none !important; }
        footer { display: none !important; }
        
        /* 2. BOTONES PRINCIPALES CÓMODOS */
        div.stButton > button:first-child {
            padding: 12px 20px !important; 
            font-weight: bold !important;  
            border-radius: 8px !important; 
        }
        
        /* 3. OPCIONES DE RESPUESTA (Letra normal, pero fáciles de pulsar con el dedo) */
        div.stRadio > div[role="radiogroup"] label {
            padding-top: 10px !important;   
            padding-bottom: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)

def init_state():
    if 'indice_actual' not in st.session_state:
        st.session_state.indice_actual = -1  
    if 'respuestas' not in st.session_state:
        st.session_state.respuestas = {}
    if 'conduce' not in st.session_state:
        st.session_state.conduce = None

def avanzar():
    st.session_state.indice_actual += 1

def retroceder():
    st.session_state.indice_actual -= 1

def reiniciar():
    st.session_state.clear()
    st.session_state.indice_actual = -1

def vista_bienvenida():
    st.title("👁️ Cuestionario de Visión Funcional")
    st.write("---")
    st.markdown("""
    Este breve cuestionario ayuda a su oftalmólogo a entender cómo afecta su pérdida de visión a su vida diaria (con sus gafas o lentillas en caso de necesitarlas). 
                
    Por favor, responda con sinceridad a las siguientes preguntas. 
    Si no realiza alguna de las siguientes actividades, marque la última opción.
    """)
    st.write("---")
    st.button("Comenzar cuestionario ➡️", on_click=avanzar, use_container_width=True)

def vista_preguntas_generales(indice):
    pregunta_actual = preguntas[indice]
    progreso = (indice + 1) / (len(preguntas) + 1)
    st.progress(progreso)
    
    st.markdown(f"### {pregunta_actual}")
    
    if pregunta_actual in imagenes_preguntas:
        try:
            st.image(imagenes_preguntas[pregunta_actual], width=350)
            st.write("") 
        except Exception as e:
            st.error("No se pudo cargar la imagen asociada.")

    respuesta_previa = list(opciones.keys())[0]
    if pregunta_actual in st.session_state.respuestas:
        for key, val in opciones.items():
            if val == st.session_state.respuestas[pregunta_actual]:
                respuesta_previa = key
                break
    
    seleccion = st.radio("Seleccione una opción:", list(opciones.keys()), 
                         index=list(opciones.keys()).index(respuesta_previa), 
                         key=f"radio_{indice}", 
                         label_visibility="collapsed")
    
    st.session_state.respuestas[pregunta_actual] = opciones[seleccion]

    st.write("---")
    col1, col2 = st.columns(2)
    with col1: st.button("Siguiente ➡️", on_click=avanzar, use_container_width=True)
    with col2: st.button("⬅️ Anterior", on_click=retroceder, use_container_width=True)

def vista_filtro_conduccion():
    st.progress(1.0)
    st.markdown("### 🚗 Conducción")
    
    indice_previo = 1 if st.session_state.conduce == "No" else 0
    conduce = st.radio("¿Actualmente conduce o prevé la necesidad de conducir?", ["Sí", "No"], index=indice_previo, key="conduce_filtro")
    st.session_state.conduce = conduce

    st.write("---")
    col1, col2 = st.columns(2)
    
    if conduce == "No":
        def saltar_a_resultados():
            st.session_state.indice_actual = len(preguntas) + len(preguntas_conduccion) + 1
        with col1: st.button("Siguiente ➡️", on_click=saltar_a_resultados, use_container_width=True)
    else:
        with col1: st.button("Siguiente ➡️", on_click=avanzar, use_container_width=True)
        
    with col2: st.button("⬅️ Anterior", on_click=retroceder, use_container_width=True)

def vista_preguntas_conduccion(indice):
    indice_cond = indice - len(preguntas) - 1
    pregunta_actual = preguntas_conduccion[indice_cond]
    
    st.markdown("### 🚗 Conducción")
    st.markdown(f"**{pregunta_actual}**")
    
    if pregunta_actual in imagenes_preguntas:
        try:
            st.image(imagenes_preguntas[pregunta_actual], width=350)
            st.write("")
        except Exception:
            pass

    respuesta_previa = list(opciones.keys())[0]
    if pregunta_actual in st.session_state.respuestas:
        for key, val in opciones.items():
            if val == st.session_state.respuestas[pregunta_actual]:
                respuesta_previa = key
                break

    seleccion = st.radio("Seleccione una opción:", list(opciones.keys()), 
                         index=list(opciones.keys()).index(respuesta_previa), 
                         key=f"radio_cond_{indice_cond}", 
                         label_visibility="collapsed")
    
    st.session_state.respuestas[pregunta_actual] = opciones[seleccion]

    st.write("---")
    col1, col2 = st.columns(2)
    
    if indice_cond == len(preguntas_conduccion) - 1:
        with col1: st.button("✅ Calcular resultados", type="primary", on_click=avanzar, use_container_width=True)
    else:
        with col1: st.button("Siguiente ➡️", on_click=avanzar, use_container_width=True)
        
    with col2: st.button("⬅️ Anterior", on_click=retroceder, use_container_width=True)

def vista_resultados():
    st.title("📋 Resultados del Cuestionario")
    st.write("---")
    
    puntos_obtenidos, puntos_maximos = calcular_resultados()

    if puntos_maximos > 0:
        porcentaje = round((puntos_obtenidos * 100) / puntos_maximos, 1)

        st.success("¡Gracias! Por favor, muestre esta pantalla a su oftalmólogo.")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.metric("Puntuación VF", f"{porcentaje} / 100")

        st.write("---")
        st.markdown("### Notas para el oftalmólogo:")
        if st.session_state.conduce == "Sí":
            st.info("🚗 Paciente conductor activo.")
        else:
            st.info("ℹ️ El paciente no conduce.")

    else:
        st.warning("El paciente ha seleccionado opciones no puntuables en todas las preguntas.")

    st.write("---")
    st.button("🔄 Nuevo paciente (Reiniciar)", on_click=reiniciar, use_container_width=True)