# 🔥 Fire The Maze

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/license-Academic%20Use-green.svg)

Un juego de laberinto 2D donde juegas como "Firey", una pequeña llama que debe escapar del laberinto mientras evita enemigos que intentan extinguirla.

## 📖 Descripción del Juego

**Fire The Maze** es un juego de aventura y estrategia donde el jugador controla a Firey, una valiente llama que ha perdido sus poderes y está atrapada en un laberinto. El objetivo es recolectar todas las llamas perdidas para recuperar la fuerza, evitar a los enemigos elementales y encontrar la salida siguiendo la ruta más segura.

### 🎯 Objetivo Principal
- **Sobrevivir** y recolectar todas las llamas perdidas
- **Evitar** a los enemigos que pueden extinguirte
- **Escapar** del laberinto siguiendo la ruta óptima
- **Usar** power-ups estratégicamente para eliminar enemigos

## 🎮 Características del Juego

### 🏃‍♂️ Mecánicas de Juego
- **Movimiento fluido** con controles WASD o flechas direccionales
- **Sistema de recolección** de llamas para desbloquear la salida
- **Power-ups temporales** que otorgan inmunidad y capacidad de eliminar enemigos
- **Pathfinding inteligente** que muestra la ruta más segura al jugador
- **Generación procedural** de laberintos únicos en cada partida

### 👾 Tipos de Enemigos
- **💧 Gota de Agua**: Velocidad media, rango de detección estándar
- **🧊 Cristal de Hielo**: Velocidad lenta, rango de detección corto pero persistente
- **🧯 Extintor**: Velocidad rápida, rango de detección amplio

### 🔋 Sistema de Power-ups
- **Llamas Azules**: Otorgan 5 segundos de inmunidad
- **Capacidad de eliminación**: Destruye enemigos al contacto durante el power-up
- **Cambio de comportamiento**: Los enemigos huyen del jugador cuando está potenciado

## 🕹️ Controles

| Tecla | Acción |
|-------|--------|
| `W` / `↑` | Mover hacia arriba |
| `A` / `←` | Mover hacia la izquierda |
| `S` / `↓` | Mover hacia abajo |
| `D` / `→` | Mover hacia la derecha |
| `F` | Alternar pantalla completa |
| `ESC` | Salir del juego |

## 🛠️ Instalación y Ejecución

### Requisitos Previos
- Python 3.8 o superior
- Pygame 2.0 o superior

### Instalación

1. **Clona el repositorio**
```bash
git clone https://github.com/tuusuario/fire-the-maze.git
cd fire-the-maze
```

2. **Instala las dependencias**
```bash
pip install pygame
```

3. **Ejecuta el juego**
```bash
python main.py
```

### Ejecución Rápida (Windows)
Si prefieres no instalar Python, puedes usar el ejecutable precompilado:
1. Descarga la carpeta `output/`
2. Ejecuta `main.exe`

## 🏗️ Arquitectura Técnica

### 🧠 Algoritmos de IA Implementados

#### Generación de Laberintos
- **Inicialización basada en grillas**
- **Backtracking recursivo aleatorizado**
- **Optimización de densidad de caminos**
- **Sistema de validación de vecinos**

#### Pathfinding
- **Algoritmo de Dijkstra** para encontrar la ruta más corta
- **Cálculo dinámico** de caminos en tiempo real
- **Sistema de pesos** que considera la proximidad de enemigos
- **Reconstrucción de rutas** optimizada

#### Comportamientos de Enemigos (Steering Behaviors)
- **Wander**: Movimiento aleatorio de patrullaje
- **Seek**: Persecución directa del jugador
- **Flee**: Huida cuando el jugador está potenciado
- **Line of Sight**: Sistema de detección visual avanzado

### 📁 Estructura del Proyecto

```
fire-the-maze/
├── main.py              # Archivo principal del juego
├── menu.py              # Sistema de menús
├── enemy.py             # Lógica de enemigos y IA
├── fire.py              # Sistema de recolección de llamas
├── gameOver.py          # Pantalla de Game Over
├── winScreen.py         # Pantalla de victoria
├── sound_manager.py     # Gestión de audio
├── assets/              # Recursos gráficos
│   ├── firePlayer.png
│   ├── waterEnemy.png
│   ├── iceEnemy.png
│   ├── extintorEnemy.png
│   ├── fireFlames.png
│   └── bluefireFlame.png
├── resources/           # Recursos de audio
│   ├── MusicGame.mp3
│   ├── PowerUP.mp3
│   ├── Immunity.mp3
│   ├── Persecution.mp3
│   ├── GameOver.mp3
│   └── Win.mp3
└── output/              # Ejecutable compilado
    └── main.exe
```

## 🎨 Capturas de Pantalla

### Menú Principal
El juego presenta un menú elegante con opciones para iniciar el juego y ver las instrucciones.

### Gameplay
- **Laberinto procedural** con paredes negras y caminos blancos
- **Ruta verde** que indica el camino más seguro al objetivo
- **Enemigos diversos** con comportamientos únicos
- **Efectos visuales** para power-ups y colisiones

### Pantallas de Victoria/Derrota
Mensajes personalizados según el tipo de enemigo que cause la derrota o al completar exitosamente el nivel.

## 🎵 Audio y Efectos

### Música de Fondo
- **Música ambiente** durante el gameplay
- **Música de menú** para la interfaz principal
- **Música de persecución** cuando los enemigos detectan al jugador

### Efectos de Sonido
- **Power-up**: Sonido al recolectar llamas normales
- **Inmunidad**: Audio especial durante el modo power-up
- **Eliminación**: Efecto al destruir enemigos
- **Victoria/Derrota**: Sonidos distintivos para cada final

## 🤝 Contribuidores

Este proyecto fue desarrollado como parte del curso "Artificial Intelligence in Video Games" en la Universidad Panamericana por:

- **Gabriel Guerra Rosales** - Implementación de algoritmos de pathfinding y generación de laberintos
- **Gabriel Zaid Gutiérrez González** - Desarrollo de sistemas de enemigos y steering behaviors  
- **Brandon Magaña Ávalos** - Diseño de interfaz y gestión de audio
- **Yahwthani Morales Gómez** - Mecánicas de juego y integración de sistemas

**Profesor**: Alfredo Emmanuel García Falcón

## 🎓 Propósito Académico

Este juego fue creado como proyecto final para demostrar la aplicación práctica de:
- **Algoritmos de pathfinding** (Dijkstra)
- **Steering behaviors** para IA de enemigos
- **Generación procedural** de contenido
- **Máquinas de estado** para gestión de juego
- **Optimización de rendimiento** en tiempo real

## 🚀 Características Técnicas Avanzadas

### Optimizaciones de Rendimiento
- **Cálculo de pesos dinámicos** para evitar enemigos en pathfinding
- **Sistema de detección por raycast** para line of sight
- **Gestión eficiente de memoria** con pooling de objetos
- **Renderizado optimizado** con superficie de pantalla adaptable

### Escalabilidad
- **Soporte para pantalla completa** y redimensionamiento
- **Sistema de grid adaptativo** según resolución
- **Configuración de dificultad** mediante parámetros ajustables

## 🐛 Solución de Problemas

### Problemas Comunes

**El juego no inicia:**
- Verifica que tengas Python 3.8+ instalado
- Instala pygame: `pip install pygame`
- Asegúrate de que todos los archivos de assets estén presentes

**Audio no funciona:**
- Verifica que los archivos en `resources/` estén disponibles
- Comprueba la configuración de audio del sistema

**Rendimiento bajo:**
- Cierra otras aplicaciones que consuman recursos
- Usa el modo pantalla completa para mejor rendimiento

## 📝 Licencia y Uso

Este proyecto fue desarrollado con fines académicos como parte del curso "Artificial Intelligence in Video Games" en la Universidad Panamericana.

### 🎓 Uso Académico y Educativo
- ✅ **Permitido**: Usar el código para aprender y estudiar algoritmos de IA
- ✅ **Permitido**: Modificar y experimentar con el código para proyectos educativos
- ✅ **Permitido**: Usar como referencia para proyectos similares (con atribución apropiada)
- ✅ **Permitido**: Compartir con otros estudiantes y profesores

### ⚖️ Términos de Uso
- **Atribución requerida**: Si usas este código como base para tu proyecto, por favor menciona a los autores originales
- **Uso no comercial**: Este proyecto está destinado para fines educativos y de aprendizaje
- **Sin garantías**: El código se proporciona "tal como está" sin garantías de ningún tipo

### 📚 Cómo Citar Este Proyecto
Si usas este proyecto como referencia en trabajos académicos:

```
Guerra, G., Gutiérrez, G. Z., Magaña, B., & Morales, Y. (2024). 
Fire The Maze: Implementación de Algoritmos de IA en Videojuegos. 
Proyecto Final - Artificial Intelligence in Video Games, 
Universidad Panamericana.
```

**Nota para Estudiantes**: Si eres estudiante y planeas usar partes de este código para tu propio proyecto académico, asegúrate de cumplir con las políticas de integridad académica de tu institución. Recomendamos usar este proyecto como referencia y aprendizaje, no como una solución completa a copiar.

## 🌟 Agradecimientos

Agradecemos especialmente al profesor Alfredo Emmanuel García Falcón por su guía durante el desarrollo del proyecto y por proporcionar las bases teóricas necesarias para implementar los algoritmos de inteligencia artificial utilizados en el juego.

---

¿Te gustó el juego? ¡Danos una ⭐ en GitHub!

## 📞 Contacto

Para preguntas sobre el desarrollo o colaboraciones, puedes contactarme por aqui o mis redes sociales ubicadas en la descripcion de mi perfil :)
