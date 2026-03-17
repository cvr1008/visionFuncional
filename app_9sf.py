import streamlit as st

# que me salga cada una en una pantalla

# Configuración para que se vea bien en móviles
st.set_page_config(page_title="Cuestionario VF", page_icon="👁️", layout="centered")

# Título y explicaciones
st.title("Cuestionario de Visión Funcional")

st.markdown("""
Este breve cuestionario ayuda a su oftalmólogo a entender cómo afecta su pérdida de visión a su vida diaria (con sus gafas o lentillas en caso de necesitarlas). 
            
Por favor, responda con sinceridad a las siguientes preguntas. Si no realiza alguna actividad por motivos que no tienen que ver con su vista, marque la última opción.
""")

st.write("---")

# DICCIONARIOS DE PUNTUACIÓN 


opciones = {
    "Sin dificultad": 4,
    "Un poco de dificultad": 3,
    "Dificultad moderada": 2,
    "Mucha dificultad": 1,
    "Incapaz de hacerlo": 0,
    "No realizo esta actividad por otros motivos": None
}

preguntas = [
    "3. Leer un periódico o un libro.",
    "4. Ver la televisión.",
    "5. Ver los precios cuando hace la compra.",
    "6. Escribir cartas/textos a mano, hacer sudokus/crucigramas, etc.",
    "7. Manejar el ordenador (trabajar con word/excel) con fines laborales.",
    "8. Manejar el teléfono móvil/ tablet.",
    "9. Cocinar",
    "10. Reconocer caras de personas por la calle.",
    "11. Leer letreros grandes en la calle, nombres de tiendas, etc.",
    "12. Identificar bordillos/escalones o irregularidades en el suelo.",
    "13. Hacer trabajos manuales finos/precisos (ej. coser, manualidades, carpintería).",
    "14. Participar en deportes (ej. petanca, tenis/pádel, golf) o ver deporte en vivo.",
    "15. Participar en sus aficiones (jugar a juegos de mesa, cartas)"
    
]

preguntas_conduccion = [
    "16. Conducir de día.", # 
    "17. Conducir de noche.",
    "18. Conducir al amanecer y/o atardecer.",
    "19. Distinguir señales de tráfico y carteles en la carretera."
    
]

# --- INICIO DE PREGUNTAS  ---
st.markdown("### Actividades de la vida diaria")
st.markdown("¿Con qué nivel de dificultad realiza estas actividades? \n")

respuestas_310 = {}
for p in preguntas:
    st.markdown(f"**{p}**")
    # Añadimos key=f"preg_{p}" para que cada una tenga un DNI único
    respuesta = st.radio("Seleccione una opción:", list(opciones.keys()), index=0, key=f"preg_{p}", label_visibility="collapsed")
    respuestas_310[p] = opciones[respuesta] 
    st.write("")

st.write("---")
st.markdown("### Conducción")
# Añadimos key="conduce_principal"
conduce = st.radio("¿Actualmente conduce o prevé la necesidad de conducir?", ["Sí", "No"], index=1, key="conduce_principal")

respuestas_conduccion = {}

if conduce == "Sí":
    for p in preguntas_conduccion:
        st.markdown(f"**{p}**")
        # Añadimos key=f"cond_{p}"
        respuesta = st.radio("Seleccione una opción:", list(opciones.keys()), index=0, key=f"cond_{p}", label_visibility="collapsed")
        respuestas_conduccion[p] = opciones[respuesta]
        st.write("")    

st.write("---")
st.markdown("### ¿Ha terminado?")

enviado = st.button("Enviar cuestionario", use_container_width=True)

# --- LÓGICA DE PUNTUACIÓN ---
if enviado:
    st.write("---")
    st.header("Resultados")
    
    
    todas_respuestas_validas = []

    respuestas_validas_310 = [valor for valor in respuestas_310.values() if valor is not None]
    todas_respuestas_validas.extend(respuestas_validas_310)
    
    respuestas_validas_cond = [valor for valor in respuestas_conduccion.values() if valor is not None]
    todas_respuestas_validas.extend(respuestas_validas_cond)

    if len(todas_respuestas_validas) > 0:
        puntuacion_total = sum(todas_respuestas_validas)
        puntuacion_max = len(todas_respuestas_validas) * 4
        porcentaje = round(puntuacion_total*100/puntuacion_max, 1)

        col1, col2 = st.columns(2)
        col1.metric("Puntuación Total Obtenida", f"{porcentaje} / 100")

        st.success("¡Gracias! Por favor, muestre esta pantalla a su oftalmólogo.")
        
        st.write("---")
        st.markdown("### Notas para el oftalmólogo:")
        if conduce == "Sí":
            st.write("• Paciente conductor activo.")

    else:
        st.warning("El paciente ha seleccionado opciones no puntuables en todas las preguntas.")