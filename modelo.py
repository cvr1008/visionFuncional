# modelo.py
import streamlit as st

opciones = {
    "Sin dificultad": 4,
    "Un poco de dificultad": 3,
    "Dificultad moderada": 2,
    "Mucha dificultad": 1,
    "Incapaz de hacerlo": 0,
    "No realizo esta actividad por otros motivos": None
}

pesos_conduccion = {
    "15. Conducir de noche.": 3,                 
    "16. Conducir al amanecer y/o atardecer.": 5,  
    "14. Conducir de día.": 7                    
}

preguntas = [
    "1. Leer un periódico o un libro.",
    "2. Ver la televisión.",
    "3. Ver los precios cuando hace la compra.",
    "4. Escribir cartas/textos a mano, hacer sudokus/crucigramas, etc.",
    "5. Manejar el ordenador (trabajar con word/excel) con fines laborales.",
    "6. Manejar el teléfono móvil/ tablet.",
    "7. Cocinar",
    "8. Reconocer caras de personas por la calle.",
    "9. Leer letreros grandes en la calle, nombres de tiendas, etc.",
    "10. Identificar bordillos/escalones o irregularidades en el suelo.",
    "11. Hacer trabajos manuales finos/precisos (ej. coser, manualidades, carpintería).",
    "12. Participar en deportes (ej. petanca, tenis/pádel, golf) o ver deporte en vivo.",
    "13. Participar en sus aficiones (jugar a juegos de mesa, cartas, pasear)"
]

preguntas_conduccion = [
    "14. Conducir de día.",
    "15. Conducir de noche.",
    "16. Conducir al amanecer y/o atardecer.",
    "17. Distinguir señales de tráfico y carteles en la carretera."
]

imagenes_preguntas = {
    "1. Leer un periódico o un libro.": "images/periodico.webp",
    "2. Ver la televisión.": "images/tele.jpg",
    "3. Ver los precios cuando hace la compra.": "images/compra.jpg",
    "4. Escribir cartas/textos a mano, hacer sudokus/crucigramas, etc.": "images/escribir.jpg",
    "5. Manejar el ordenador (trabajar con word/excel) con fines laborales.": "images/ordenador.webp",
    "6. Manejar el teléfono móvil/ tablet.": "images/movil.webp",
    "7. Cocinar":"images/cocinar.jpeg",
    "8. Reconocer caras de personas por la calle.": "images/encontrarse_gente.jpeg",
    "9. Leer letreros grandes en la calle, nombres de tiendas, etc.": "images/letreros_calle.jpg",
    "10. Identificar bordillos/escalones o irregularidades en el suelo.": "images/adoquin.jpg",
    "11. Hacer trabajos manuales finos/precisos (ej. coser, manualidades, carpintería).": "images/destornillador.webp",
    "12. Participar en deportes (ej. petanca, tenis/pádel, golf) o ver deporte en vivo.": "images/golf.avif",
    "13. Participar en sus aficiones (jugar a juegos de mesa, cartas, pasear)": "images/cartas.jpg"
}

def calcular_resultados():
    puntos_obtenidos = 0
    puntos_maximos = 0
    
    for p in preguntas:
        if p in st.session_state.respuestas and st.session_state.respuestas[p] is not None:
            peso = pesos_conduccion.get(p, 1) 
            puntos_obtenidos += st.session_state.respuestas[p] * peso
            puntos_maximos += 4 * peso
            
    if st.session_state.conduce == "Sí":
        for p in preguntas_conduccion:
            if p in st.session_state.respuestas and st.session_state.respuestas[p] is not None:
                peso = pesos_conduccion.get(p, 1)
                puntos_obtenidos += st.session_state.respuestas[p] * peso
                puntos_maximos += 4 * peso
                
    return puntos_obtenidos, puntos_maximos