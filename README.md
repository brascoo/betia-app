# BETIA Pro 🎯

BETIA Pro es una aplicación web full-stack diseñada para la gestión, seguimiento y análisis de apuestas deportivas (Picks y Parleys). Integra una interfaz moderna y características de inteligencia artificial para ayudar a los apostadores a tomar mejores decisiones y gestionar su bankroll de manera efectiva.

## Características Principales 🚀

*   **Autenticación y Seguridad:** Sistema multiusuario con registro seguro (encriptación bcrypt) y manejo de sesiones mediante tokens JWT.
*   **Gestión de Picks y Parleys:** Registra tus selecciones individuales y combinadas en la base de datos, indicando cuota, stake y confianza.
*   **Seguimiento de Bankroll:** Controla tus ganancias, pérdidas y la evolución de tu capital base por usuario.
*   **Análisis IA (Integración con Google Gemini):** Utiliza la inteligencia artificial para analizar enfrentamientos, ligas y encontrar valor en las cuotas basándose en contexto adicional.
*   **Resultados e Historial:** Visualiza la evolución de tu bankroll en un gráfico interactivo y mantén un registro de todas tus apuestas.
*   **Soporte Multideporte:** Adaptado principalmente para Fútbol ⚽, Baloncesto 🏀 y Tenis 🎾, con soporte para otros deportes.
*   **Modo Claro / Oscuro:** Interfaz adaptable a tus preferencias visuales.

## Tecnologías 💻

El proyecto ha evolucionado a una arquitectura Full-Stack compuesta por:

### Frontend
*   **HTML5 & CSS3** (Variables CSS, Grid, Flexbox, Diseño Responsivo)
*   **JavaScript (Vanilla)**
*   Uso de `fetch API` para interactuar de forma asíncrona con el servidor.

### Backend
*   **Python 3.10+**
*   **FastAPI** (Framework web ultrarrápido)
*   **SQLite** (Base de datos ligera)
*   **SQLAlchemy** (ORM para modelado de datos)
*   **PyJWT & Bcrypt** (Autenticación y seguridad)

## Instalación y Uso 🛠️

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/brascoo/betia-app.git
    cd betia-app
    ```

2.  **Instala las dependencias de Python:**
    Es recomendable usar un entorno virtual, pero también puedes instalarlo a nivel de usuario:
    ```bash
    pip3 install -r requirements.txt
    ```

3.  **Inicia el servidor backend:**
    Esto creará automáticamente el archivo de base de datos (`database.db`) si no existe.
    ```bash
    python3 -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
    ```

4.  **Abre el cliente web:**
    Simplemente haz doble clic en el archivo `index.html` o ábrelo en tu navegador favorito.
    ```bash
    # En Linux o macOS, puedes usar:
    open index.html # Mac
    xdg-open index.html # Linux
    ```

5.  Crea tu cuenta desde el modal de Inicio de Sesión y empieza a utilizar la app.

## Configuración de la IA (Google Gemini) 🤖

Para habilitar la función de "Análisis IA" dentro de la aplicación:
1. Asegúrate de haber iniciado sesión.
2. Ve a la sección **Análisis IA**.
3. Ingresa tu API Key de Google Gemini en la configuración (puedes obtener una clave gratuita en [Google AI Studio](https://aistudio.google.com/app/apikey)).
4. Haz clic en "Guardar Key". Las consultas de análisis utilizarán esta clave de forma local en tu navegador para comunicarse con Google.
