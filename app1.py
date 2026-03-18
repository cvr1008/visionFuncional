import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Cuestionario VF", page_icon="👁️", layout="centered")

# --- SISTEMA DE NAVEGACIÓN (Paginación) ---
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

# --- DICCIONARIOS Y PREGUNTAS ---
opciones = {
    "Sin dificultad": 4,
    "Un poco de dificultad": 3,
    "Dificultad moderada": 2,
    "Mucha dificultad": 1,
    "Incapaz de hacerlo": 0,
    "No realizo esta actividad por otros motivos": None
}

# --- SISTEMA DE PESOS CLÍNICOS ---
# Las preguntas normales tienen un peso de 1.
# Aplicamos la escala 30% (3), 50% (5) y 70% (7) a la conducción.
pesos_preguntas = {
    "15. Conducir de noche.": 3,                 # 30% de gravedad relativa
    "16. Conducir al amanecer y/o atardecer.": 5,  # 50% de gravedad relativa
    "14. Conducir de día.": 7                    # 70% de gravedad relativa
}

preguntas = [
    "1. 📖 Leer un periódico o un libro.",
    "2. 📺 Ver la televisión.",
    "3. Ver los precios cuando hace la compra.",
    "4. ✒️ Escribir cartas/textos a mano, hacer sudokus/crucigramas, etc.",
    "5. 💻 Manejar el ordenador (trabajar con word/excel) con fines laborales.",
    "6. 📱 Manejar el teléfono móvil/ tablet.",
    "7. 🍳 Cocinar",
    "8. Reconocer caras de personas por la calle.",
    "9. Leer letreros grandes en la calle, nombres de tiendas, etc.",
    "10. Identificar bordillos/escalones o irregularidades en el suelo.",
    "11. 🧵 Hacer trabajos manuales finos/precisos (ej. coser, manualidades, carpintería).",
    "12. 🏌️🏓 Participar en deportes (ej. petanca, tenis/pádel, golf) o ver deporte en vivo.",
    "13. 🎮 Participar en sus aficiones (jugar a juegos de mesa, cartas, pasear)"
]

preguntas_conduccion = [
    "14. ☀️ Conducir de día.",
    "15. 🌃 Conducir de noche.",
    "16. 🌄 Conducir al amanecer y/o atardecer.",
    "17. 🛑🚸 Distinguir señales de tráfico y carteles en la carretera."
]

# DICCIONARIO DE IMÁGENES 
# Aquí enlazas el texto exacto de la pregunta con su foto.
imagenes_preguntas = {
    "1. 📖 Leer un periódico o un libro.": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=500&q=80" # Foto de prueba de internet
    # Cuando quieras añadir más, solo tienes que poner una coma arriba y añadir la siguiente línea, por ejemplo:
    # "2. 📺 Ver la televisión.": "foto_tele.jpg"
}

# --- CABECERA FIJA ---
st.title("👁️ Cuestionario de Visión Funcional")
st.write("---")

# ==========================================
# PANTALLA 0: Bienvenida (-1)
# ==========================================
if st.session_state.indice_actual == -1:
    st.markdown("""
    Este breve cuestionario ayuda a su oftalmólogo a entender cómo afecta su pérdida de visión a su vida diaria (con sus gafas o lentillas en caso de necesitarlas). 
                
    Por favor, responda con sinceridad a las siguientes preguntas. Si no realiza alguna actividad por motivos que no tienen que ver con su vista, marque la última opción.
    """)
    st.write("---")
    st.button("Comenzar cuestionario ➡️", on_click=avanzar, use_container_width=True)

# ==========================================
# PANTALLA 1: Preguntas de la 3 a la 15
# ==========================================
elif 0 <= st.session_state.indice_actual < len(preguntas):
    pregunta_actual = preguntas[st.session_state.indice_actual]
    progreso = (st.session_state.indice_actual + 1) / (len(preguntas) + 1)
    st.progress(progreso)
    
    st.markdown(f"### {pregunta_actual}")
    
    # MOSTRAR LA IMAGEN SI EXISTE ---
    # Busca si la pregunta actual está en nuestro diccionario de imágenes
    if pregunta_actual in imagenes_preguntas:
        try:
            # Pinta la imagen ocupando el ancho del móvil
            st.image(imagenes_preguntas[pregunta_actual], use_container_width=True)
            st.write("") # Espaciador
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
                         key=f"radio_{st.session_state.indice_actual}", 
                         label_visibility="collapsed")
    
    st.session_state.respuestas[pregunta_actual] = opciones[seleccion]

    st.write("---")
    col1, col2 = st.columns(2)
    with col1: st.button("⬅️ Anterior", on_click=retroceder, use_container_width=True)
    with col2: st.button("Siguiente ➡️", on_click=avanzar, use_container_width=True)

# ==========================================
# PANTALLA 2: Filtro de Conducción
# ==========================================
elif st.session_state.indice_actual == len(preguntas):
    st.progress(1.0)
    st.markdown("### 🚗 Conducción")
    
    indice_previo = 1 if st.session_state.conduce == "No" else 0
    conduce = st.radio("¿Actualmente conduce o prevé la necesidad de conducir?", ["Sí", "No"], index=indice_previo, key="conduce_filtro")
    st.session_state.conduce = conduce

    st.write("---")
    col1, col2 = st.columns(2)
    with col1: st.button("⬅️ Anterior", on_click=retroceder, use_container_width=True)
    
    if conduce == "No":
        def saltar_a_resultados():
            st.session_state.indice_actual = len(preguntas) + len(preguntas_conduccion) + 1
        with col2: st.button("Siguiente ➡️", on_click=saltar_a_resultados, use_container_width=True)
    else:
        with col2: st.button("Siguiente ➡️", on_click=avanzar, use_container_width=True)

# ==========================================
# PANTALLA 3: Preguntas de Conducción (16-19)
# ==========================================
elif len(preguntas) < st.session_state.indice_actual <= len(preguntas) + len(preguntas_conduccion):
    indice_cond = st.session_state.indice_actual - len(preguntas) - 1
    pregunta_actual = preguntas_conduccion[indice_cond]
    
    st.markdown("### 🚗 Conducción")
    st.markdown(f"**{pregunta_actual}**")
    
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
    with col1: st.button("⬅️ Anterior", on_click=retroceder, use_container_width=True)
    
    if indice_cond == len(preguntas_conduccion) - 1:
        with col2: st.button("✅ Calcular resultados", type="primary", on_click=avanzar, use_container_width=True)
    else:
        with col2: st.button("Siguiente ➡️", on_click=avanzar, use_container_width=True)

# ==========================================
# PANTALLA 4: Resultados
# ==========================================
else:
    st.header("📋 Resultados")
    
    puntos_obtenidos = 0
    puntos_maximos = 0
    
    for p in preguntas:
        if p in st.session_state.respuestas and st.session_state.respuestas[p] is not None:
            peso = pesos_preguntas.get(p, 1) 
            puntos_obtenidos += st.session_state.respuestas[p] * peso
            puntos_maximos += 4 * peso
            
    if st.session_state.conduce == "Sí":
        for p in preguntas_conduccion:
            if p in st.session_state.respuestas and st.session_state.respuestas[p] is not None:
                peso = pesos_preguntas.get(p, 1)
                puntos_obtenidos += st.session_state.respuestas[p] * peso
                puntos_maximos += 4 * peso

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