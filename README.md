# README - Space Defender: Ultra Strike

## 1. DESCRIPCIÓN GENERAL
Space Defender es un videojuego de acción arcade donde el jugador toma el control de una nave defensora. Aquí el objetivo es interceptar y destruir las naces enemigas antes de que logren traspasar la línea de defensa o colisionen con el jugador. El juego cuenta con una estética moderna de neón y una dificultad progresiva.

---

## 2. REQUISITOS DEL PROYECTO (CRITERIOS)
El proyecto cumple con los parámetros solicitados:

* **Uso de Pygame:** Se realiza la implementación completa utilizando el motor Pygame estándar.
* **Funciones Personalizadas:** El código está modularizado con funciones para dibujo (`draw_text`), interfaces (`draw_glass_panel`) y lógica de estados (`show_game_over`).
* **Enemigos:** Hay un sistema de generación de tres tipos de enemigos (básico, rápidos y tanques) cada uno con diferentes velocidades y puntos de vida.
* **Menús:** Flujo de usuario completo que incluye el Menú de Inicio y la Pantalla de Fin de Misión.

---

## 3. CARACTERÍSTICAS TÉCNICAS
* **Clases POO:** Se han creado clases para gestionar el comportamiento del jugador (`Player`), los Enemigos (`Enemy`) y los efectos de explosión (`Particle`).
* **Dificultad Dinámica:** El nivel del juego aumenta cada 8 enemigos derrotados, haciendo que aparezcan más rápido y se muevan con mayor velocidad.
* **Interfaz de Usuario:** Panel inferior que muestra en tiempo real la puntuación, el nivel actual y el estado de los escudos (vidas).

---

## 4. INSTRUCCIONES DE JUEGO

### Controles:
* **Movimiento:** Teclas `A`/`D` o Flechas Izquierda / Derecha.
* **Disparar:** Barra Espaciadora.
* **Menús:** Uso del ratón para hacer clic en los botones.

### Mecánicas:
1. Comienzas con 3 escudos (vidas).
2. Pierdes un escudo si un enemigo te toca o si llega al final de la pantalla.
3. El juego termina cuando tus escudos llegan a cero.
4. Intenta alcanzar el nivel más alto eliminando enemigos para sumar puntos.

---

## 5. CÓMO EJECUTAR
1. Instalar Python.
2. Instalar la librería requerida: `pip install pygame`.
3. Ejecutar el script: `python space_defender.py`