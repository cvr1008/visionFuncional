import streamlit as st

# Configuración para que se vea bien en móviles
st.set_page_config(page_title="Cuestionario VF-14", page_icon="👁️", layout="centered")

# Título y explicaciones
st.title("Cuestionario de Visión Funcional")
st.markdown("""
Este breve cuestionario ayuda a su oftalmólogo a entender cómo afecta su visión a su vida diaria.

Por favor, indique el grado de dificultad que tiene al realizar las siguientes actividades (incluso cuando usa sus gafas o lentillas habituales). Si no realiza alguna actividad por motivos que no tienen que ver con su vista, marque la última opción.
""")

st.write("---")

# Las opciones de respuesta y sus valores
opciones = {
    "Sin dificultad": 4,
    "Un poco de dificultad": 3,
    "Dificultad moderada": 2,
    "Mucha dificultad": 1,
    "Incapaz de hacerlo": 0,
    "No realizo esta actividad por otros motivos": None
}

# PREGUNTA CONDICIONAL (Fuera del formulario principal)
st.markdown("### Conducción")
conduce = st.radio("¿Actualmente conduce o prevé la necesidad de conducir?", ["Sí", "No"], index=1)

st.write("---")

# Las 14 preguntas oficiales del VF-14
preguntas = [
    "1. Leer letra pequeña (ej. prospectos de medicinas, guía telefónica).",
    "2. Leer un periódico o un libro.",
    "3. Leer letreros grandes en la calle o nombres de tiendas.",
    "4. Ver los escalones, escaleras o bordillos.",
    "5. Hacer trabajos manuales finos/precisos (ej. coser, tejer, carpintería).",
    "6. Escribir cheques/cartas, rellenar impresos o usar el teclado.",
    "7. Jugar a juegos de mesa (ej. cartas, dominó, bingo, ajedrez).",
    "8. Participar en deportes (ej. petanca, tenis/pádel, golf) o ver deporte en vivo.",
    "9. Cocinar.",
    "10. Ver la televisión.",
    "11. Reconocer caras de personas a media distancia."
    "12. Distinguir señales de tráfico y semáforos caminando."
]

preguntas_conduccion = [
    "13. Conducir de día.",
    "14. Conducir de noche."
    "15. Distinguir señales de tráfico y semáforos en coche o bicicleta."
    
]

respuestas_usuario = []

# FORMULARIO PRINCIPAL
with st.form("vf14_form"):
    st.markdown("### Preguntas sobre su visión")
    st.markdown("¿Con qué nivel de dificultad se desenvuelve a la hora de realizar estas actividades?")
    
    # 1. Mostramos las preguntas de la 1 a la 11
    for p in preguntas:
        st.markdown(f"**{p}**")
        respuesta = st.radio("Seleccione una opción:", list(opciones.keys()), index=0, key=p, label_visibility="collapsed")
        respuestas_usuario.append(opciones[respuesta])
        st.write("")
        
    # 2. Mostramos las de conducción SOLO si marcó "Sí" arriba
    if conduce == "Sí":
        for p in preguntas_conduccion:
            st.markdown(f"**{p}**")
            respuesta = st.radio("Seleccione una opción:", list(opciones.keys()), index=0, key=p, label_visibility="collapsed")
            respuestas_usuario.append(opciones[respuesta])
            st.write("")
    
    st.markdown("### ¿Ha terminado?")
    enviado = st.form_submit_button("Calcular mi puntuación", use_container_width=True)

# Lógica de cálculo al pulsar el botón
if enviado:
    respuestas_validas = [r for r in respuestas_usuario if r is not None]
    
    if len(respuestas_validas) > 0:
        puntuacion_maxima_posible = len(respuestas_validas) * 4
        suma_puntuaciones = sum(respuestas_validas)
        # Fórmula matemática del VF-14
        indice_vf14 = (suma_puntuaciones / puntuacion_maxima_posible) * 100
        
        st.write("---")
        st.success("¡Gracias! Por favor, muestre esta pantalla a su oftalmólogo al entrar en la consulta.")
        
        # Mostrar el resultado muy grande para que el médico lo vea fácil
        st.metric(label="Puntuación VF-14", value=f"{indice_vf14:.1f} / 100")
            
    else:
        st.error("Por favor, conteste al menos a una pregunta válida para poder calcular el resultado.")